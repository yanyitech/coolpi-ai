/**
 * @file ocr_rec model
 */


import { Runner, env } from '@paddlejs/paddlejs-core';
import '@paddlejs/paddlejs-backend-webgl';
import { BOX, POINTS, POINT } from "./type"
import DBProcess from './dbPostprocess';
import RecProcess from './recPostprocess';
import cv from '@paddlejs-mediapipe/opencv/library/opencv_ocr';
import { flatten, int, clip } from './util';

export interface DrawBoxOptions {
    canvas?: HTMLCanvasElement;
    style?: CanvasStyleOptions;
}

export interface CanvasStyleOptions {
    strokeStyle?: string;
    lineWidth?: number;
    fillStyle?: string;
}

export interface DetPostConfig {
    shape: number;
    thresh: number;
    box_thresh: number;
    unclip_ratio: number;
}
const defaultPostConfig: DetPostConfig = {shape: 960, thresh: 0.3, box_thresh: 0.6, unclip_ratio:1.5};

let DEFAULTDETSHAPE = 960;
let RECWIDTH = 320;
let RECHEIGHT = 48;
const canvas_det = document.createElement('canvas') as HTMLCanvasElement;
const canvas_rec = document.createElement('canvas') as HTMLCanvasElement;
let detectRunner = null as Runner;
let recRunner = null as Runner;

initCanvas(canvas_det);
initCanvas(canvas_rec);

function initCanvas(canvas: HTMLCanvasElement) {
    canvas.style.position = 'fixed';
    canvas.style.bottom = '0';
    canvas.style.zIndex = '-1';
    canvas.style.opacity = '0';
    document.body.appendChild(canvas);
}

export async function init(detCustomModel = '', recCustomModel = '') {
    const detModelPath = 'https://js-models.bj.bcebos.com/PaddleOCR/PP-OCRv3/ch_PP-OCRv3_det_infer_js_960/model.json';
    const recModelPath = 'https://js-models.bj.bcebos.com/PaddleOCR/PP-OCRv3/ch_PP-OCRv3_rec_infer_js/model.json';
    env.set('webgl_pack_output', true);
    detectRunner = new Runner({
        modelPath: detCustomModel ? detCustomModel : detModelPath,
        fill: '#fff',
        mean: [0.485, 0.456, 0.406],
        std: [0.229, 0.224, 0.225],
        bgr: true,
        webglFeedProcess: true
    });
    const detectInit = detectRunner.init();

    recRunner = new Runner({
        modelPath: recCustomModel ? recCustomModel : recModelPath,
        fill: '#000',
        mean: [0.5, 0.5, 0.5],
        std: [0.5, 0.5, 0.5],
        bgr: true,
        webglFeedProcess: true
    });
    const recInit = recRunner.init();

    await Promise.all([detectInit, recInit]);

    if (detectRunner.feedShape) {
        DEFAULTDETSHAPE = detectRunner.feedShape.fw;
    }
    if (recRunner.feedShape) {
        RECWIDTH = recRunner.feedShape.fw;
        RECHEIGHT = recRunner.feedShape.fh;
    }

}

async function detect(image: HTMLImageElement, Config:DetPostConfig = defaultPostConfig) {
    // ????????????
    const DETSHAPE = Config.shape ? Config.shape : DEFAULTDETSHAPE;
    const thresh = Config.thresh;
    const box_thresh = Config.box_thresh;
    const unclip_ratio = Config.unclip_ratio;

    const targetWidth = DETSHAPE;
    const targetHeight = DETSHAPE;
    canvas_det.width = targetWidth;
    canvas_det.height = targetHeight;
    // ??????canvas??????????????????????????????????????????
    const ctx = canvas_det.getContext('2d');
    ctx!.fillStyle = '#fff';
    ctx!.fillRect(0, 0, targetHeight, targetWidth);
    // ??????????????????
    let sw = targetWidth;
    let sh = targetHeight;
    let x = 0;
    let y = 0;
    // target?????????????????? ????????????????????????target?????????
    if (targetWidth / targetHeight * image.naturalHeight / image.naturalWidth >= 1) {
        sw = Math.round(sh * image.naturalWidth / image.naturalHeight);
        x = Math.floor((targetWidth - sw) / 2);
    }
    // target?????????????????? ????????????????????????target?????????
    else {
        sh = Math.round(sw * image.naturalHeight / image.naturalWidth);
        y = Math.floor((targetHeight - sh) / 2);
    }
    ctx!.drawImage(image, x, y, sw, sh);
    const shapeList = [DETSHAPE, DETSHAPE];
    const outsDict = await detectRunner.predict(canvas_det);
    const postResult = new DBProcess(outsDict, shapeList, thresh, box_thresh, unclip_ratio);
    // ????????????
    const result = postResult.outputBox();
    // ??????????????????
    const points = JSON.parse(JSON.stringify(result.boxes));
    // ??????????????????
    const adjust = 8;
    points && points.forEach((item: [number, number][]) => {
        item.forEach((point, index) => {
            // ???????????????????????????????????????
            point[0] = clip(
                (Math.round(point[0] - x) * Math.max(image.naturalWidth, image.naturalHeight) / DETSHAPE)
                + (index === 0 ? -adjust : index === 1 ? adjust : index === 2 ? adjust : -adjust),
                0,
                image.naturalWidth
            );
            point[1] = clip(
                (Math.round(point[1] - y) * Math.max(image.naturalWidth, image.naturalHeight) / DETSHAPE)
                + (index === 0 ? -adjust : index === 1 ? -adjust : index === 2 ? adjust : adjust),
                0,
                image.naturalHeight
            );
        });
    });
    return points;
}

function drawBox(
    points: [[number, number], [number, number], [number, number], [number, number]][],
    image: HTMLImageElement,
    canvas: HTMLCanvasElement,
    style?: CanvasStyleOptions
) {
    canvas.width = image.naturalWidth;
    canvas.height = image.naturalHeight;
    const ctx = canvas.getContext('2d');
    ctx!.drawImage(image, 0, 0, canvas.width, canvas.height);
    points && points.forEach((point: [number, number][] )=> {
        // ??????????????????????????????
        ctx!.beginPath();
        // ??????????????????????????????????????????
        ctx!.strokeStyle = style?.strokeStyle || '#000';
        // ??????????????????????????????1
        ctx!.lineWidth = style?.lineWidth || 1;
        // ?????????????????????????????????
        ctx!.fillStyle = style?.fillStyle || 'transparent';
        // ????????????????????????
        ctx!.moveTo(point[0][0], point[0][1]);
        ctx!.lineTo(point[1][0], point[1][1]);
        ctx!.lineTo(point[2][0], point[2][1]);
        ctx!.lineTo(point[3][0], point[3][1]);
        // ??????????????????
        ctx!.fill();
        ctx!.closePath();
        ctx!.stroke();
        ctx!.restore();
    });
}

/**
 * ????????????
 * @param {HTMLImageElement} image ??????
 * @param {Object} options ???????????????????????????
 * @param detConfig ????????????????????????
 */
export async function recognize(
    image: HTMLImageElement,
    options?: DrawBoxOptions,
    detConfig:DetPostConfig = defaultPostConfig
) {
    // ?????????????????????
    const point = await detect(image, detConfig);
    // ???????????????
    if (options?.canvas) {
        drawBox(point, image, options.canvas, options.style);
    }
    const boxes = sorted_boxes(point);
    const text_list: string[] = [];
    for (let i = 0; i < boxes.length; i++) {
        const tmp_box = JSON.parse(JSON.stringify(boxes[i]));
        get_rotate_crop_image(image, tmp_box);
        // ??????ratio=3???3?????????????????????????????????????????????
        const ratio = 3;
        const width_num = Math.ceil(canvas_det.width / RECWIDTH / ratio);
        let text_list_tmp = '';
        /**
         * ????????????????????????????????????box????????? > ratio * RECWIDTH????????? ratio * RECWIDTH????????????????????????????????????????????????????????????????????????
         * ????????????????????????????????????box????????? < ratio * RECWIDTH????????????????????????
         */
        if (width_num > 1){
            // ??????ratio*RECWIDTH????????????????????????
            for (let i = 0; i < width_num; i++) {
                resize_norm_img_splice(canvas_det, canvas_det.width, canvas_det.height, i, ratio);
                const output = await recRunner.predict(canvas_rec);
                const recResult = new RecProcess(output);
                const text = recResult.outputResult();
                text_list_tmp = text_list_tmp.concat(text.text);
            }
        } else {
            // ????????????????????????
            const output = await recRunner.predict(canvas_det);
            const recResult = new RecProcess(output);
            const text = recResult.outputResult();
            text_list_tmp = text_list_tmp.concat(text.text);
        }

        text_list.push(text_list_tmp);
    }
    return { text: text_list, points: point };
}

function sorted_boxes(box: BOX) {
    function sortNumber(a: POINTS, b: POINTS) {
        return a[0][1] - b[0][1];
    }

    const boxes = box.sort(sortNumber);
    const num_boxes = boxes.length;
    for (let i = 0; i < num_boxes - 1; i++) {
        if (Math.abs(boxes[i + 1][0][1] - boxes[i][0][1]) < 10
            && boxes[i + 1][0][0] < boxes[i][0][0]) {
            const tmp = boxes[i];
            boxes[i] = boxes[i + 1];
            boxes[i + 1] = tmp;
        }
    }
    return boxes;
}

function get_rotate_crop_image(img: HTMLCanvasElement | HTMLImageElement, points: POINTS) {
    const img_crop_width = int(Math.max(
        linalg_norm(points[0], points[1]),
        linalg_norm(points[2], points[3])
    ));
    const img_crop_height = int(Math.max(
        linalg_norm(points[0], points[3]),
        linalg_norm(points[1], points[2])
    ));
    const pts_std = [
        [0, 0],
        [img_crop_width, 0],
        [img_crop_width, img_crop_height],
        [0, img_crop_height]
    ];
    const srcTri = cv.matFromArray(4, 1, cv.CV_32FC2, flatten(points));
    const dstTri = cv.matFromArray(4, 1, cv.CV_32FC2, flatten(pts_std));
    // ?????????????????????
    const M = cv.getPerspectiveTransform(srcTri, dstTri);
    const src = cv.imread(img);
    const dst = new cv.Mat();
    const dsize = new cv.Size(img_crop_width, img_crop_height);
    // ????????????
    cv.warpPerspective(src, dst, M, dsize, cv.INTER_CUBIC, cv.BORDER_REPLICATE, new cv.Scalar());
    const dst_img_height = dst.matSize[0];
    const dst_img_width = dst.matSize[1];
    let dst_rot;
    // ????????????
    if (dst_img_height / dst_img_width >= 1.5) {
        dst_rot = new cv.Mat();
        const dsize_rot = new cv.Size(dst.rows, dst.cols);
        const center = new cv.Point(dst.cols / 2, dst.cols / 2);
        const M = cv.getRotationMatrix2D(center, 90, 1);
        cv.warpAffine(dst, dst_rot, M, dsize_rot, cv.INTER_CUBIC, cv.BORDER_REPLICATE, new cv.Scalar());
    }

    const dst_resize = new cv.Mat();
    const dsize_resize = new cv.Size(0, 0);
    let scale;
    if (dst_rot) {
        scale = RECHEIGHT / dst_rot.matSize[0];
        cv.resize(dst_rot, dst_resize, dsize_resize, scale, scale, cv.INTER_AREA);
        dst_rot.delete();
    }
    else {
        scale = RECHEIGHT / dst_img_height;
        cv.resize(dst, dst_resize, dsize_resize, scale, scale, cv.INTER_AREA);
    }
    canvas_det.width = dst_resize.matSize[1];
    canvas_det.height = dst_resize.matSize[0];
    cv.imshow(canvas_det, dst_resize);

    src.delete();
    dst.delete();
    dst_resize.delete();
    srcTri.delete();
    dstTri.delete();
}

function linalg_norm(x: POINT, y: POINT) {
    return Math.sqrt(Math.pow(x[0] - y[0], 2) + Math.pow(x[1] - y[1], 2));
}

function resize_norm_img_splice(
    image: HTMLImageElement | HTMLCanvasElement,
    origin_width: number,
    origin_height: number,
    index = 0,
    ratio = 3,
) {
    canvas_rec.width = RECWIDTH;
    canvas_rec.height = RECHEIGHT;
    const ctx = canvas_rec.getContext('2d');
    ctx!.fillStyle = '#fff';
    ctx!.clearRect(0, 0, canvas_rec.width, canvas_rec.height);
    ctx!.drawImage(image, -index * RECWIDTH * ratio, 0, origin_width, origin_height);
}
