# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import fastdeploy as fd
import cv2
import os


def parse_arguments():
    import argparse
    import ast
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--det_model", required=True, help="Path of Detection model of PPOCR.")
    parser.add_argument(
        "--cls_model",
        required=True,
        help="Path of Classification model of PPOCR.")
    parser.add_argument(
        "--rec_model",
        required=True,
        help="Path of Recognization model of PPOCR.")
    parser.add_argument(
        "--rec_label_file",
        required=True,
        help="Path of Recognization model of PPOCR.")
    parser.add_argument(
        "--image", type=str, required=True, help="Path of test image file.")
    parser.add_argument(
        "--device",
        type=str,
        default='cpu',
        help="Type of inference device, support 'cpu', 'kunlunxin' or 'gpu'.")
    parser.add_argument(
        "--backend",
        type=str,
        default="default",
        help="Type of inference backend, support ort/trt/paddle/openvino, default 'openvino' for cpu, 'tensorrt' for gpu"
    )
    parser.add_argument(
        "--device_id",
        type=int,
        default=0,
        help="Define which GPU card used to run model.")
    parser.add_argument(
        "--cpu_thread_num",
        type=int,
        default=9,
        help="Number of threads while inference on CPU.")
    parser.add_argument(
        "--cls_bs",
        type=int,
        default=1,
        help="Classification model inference batch size.")
    parser.add_argument(
        "--rec_bs",
        type=int,
        default=6,
        help="Recognition model inference batch size")
    return parser.parse_args()


def build_option(args):

    det_option = fd.RuntimeOption()
    cls_option = fd.RuntimeOption()
    rec_option = fd.RuntimeOption()

    det_option.set_cpu_thread_num(args.cpu_thread_num)
    cls_option.set_cpu_thread_num(args.cpu_thread_num)
    rec_option.set_cpu_thread_num(args.cpu_thread_num)

    if args.device.lower() == "gpu":
        det_option.use_gpu(args.device_id)
        cls_option.use_gpu(args.device_id)
        rec_option.use_gpu(args.device_id)

    if args.device.lower() == "kunlunxin":
        det_option.use_kunlunxin()
        cls_option.use_kunlunxin()
        rec_option.use_kunlunxin()

        return det_option, cls_option, rec_option

    if args.backend.lower() == "trt":
        assert args.device.lower(
        ) == "gpu", "TensorRT backend require inference on device GPU."
        det_option.use_trt_backend()
        cls_option.use_trt_backend()
        rec_option.use_trt_backend()

        # ??????trt input shape
        # ???????????????????????????????????????????????????shape, ??????????????????????????????????????????????????????32?????????.
        det_option.set_trt_input_shape("x", [1, 3, 64, 64], [1, 3, 640, 640],
                                       [1, 3, 960, 960])
        cls_option.set_trt_input_shape("x", [1, 3, 48, 10],
                                       [args.cls_bs, 3, 48, 320],
                                       [args.cls_bs, 3, 48, 1024])
        rec_option.set_trt_input_shape("x", [1, 3, 48, 10],
                                       [args.rec_bs, 3, 48, 320],
                                       [args.rec_bs, 3, 48, 2304])

        # ???????????????TRT???????????????????????????
        det_option.set_trt_cache_file(args.det_model + "/det_trt_cache.trt")
        cls_option.set_trt_cache_file(args.cls_model + "/cls_trt_cache.trt")
        rec_option.set_trt_cache_file(args.rec_model + "/rec_trt_cache.trt")

    elif args.backend.lower() == "pptrt":
        assert args.device.lower(
        ) == "gpu", "Paddle-TensorRT backend require inference on device GPU."
        det_option.use_trt_backend()
        det_option.enable_paddle_trt_collect_shape()
        det_option.enable_paddle_to_trt()

        cls_option.use_trt_backend()
        cls_option.enable_paddle_trt_collect_shape()
        cls_option.enable_paddle_to_trt()

        rec_option.use_trt_backend()
        rec_option.enable_paddle_trt_collect_shape()
        rec_option.enable_paddle_to_trt()

        # ??????trt input shape
        # ???????????????????????????????????????????????????shape, ??????????????????????????????????????????????????????32?????????.
        det_option.set_trt_input_shape("x", [1, 3, 64, 64], [1, 3, 640, 640],
                                       [1, 3, 960, 960])
        cls_option.set_trt_input_shape("x", [1, 3, 48, 10],
                                       [args.cls_bs, 3, 48, 320],
                                       [args.cls_bs, 3, 48, 1024])
        rec_option.set_trt_input_shape("x", [1, 3, 48, 10],
                                       [args.rec_bs, 3, 48, 320],
                                       [args.rec_bs, 3, 48, 2304])

        # ???????????????TRT???????????????????????????
        det_option.set_trt_cache_file(args.det_model)
        cls_option.set_trt_cache_file(args.cls_model)
        rec_option.set_trt_cache_file(args.rec_model)

    elif args.backend.lower() == "ort":
        det_option.use_ort_backend()
        cls_option.use_ort_backend()
        rec_option.use_ort_backend()

    elif args.backend.lower() == "paddle":
        det_option.use_paddle_infer_backend()
        cls_option.use_paddle_infer_backend()
        rec_option.use_paddle_infer_backend()

    elif args.backend.lower() == "openvino":
        assert args.device.lower(
        ) == "cpu", "OpenVINO backend require inference on device CPU."
        det_option.use_openvino_backend()
        cls_option.use_openvino_backend()
        rec_option.use_openvino_backend()

    return det_option, cls_option, rec_option


args = parse_arguments()

# Detection??????, ???????????????
det_model_file = os.path.join(args.det_model, "inference.pdmodel")
det_params_file = os.path.join(args.det_model, "inference.pdiparams")
# Classification??????????????????????????????
cls_model_file = os.path.join(args.cls_model, "inference.pdmodel")
cls_params_file = os.path.join(args.cls_model, "inference.pdiparams")
# Recognition???????????????????????????
rec_model_file = os.path.join(args.rec_model, "inference.pdmodel")
rec_params_file = os.path.join(args.rec_model, "inference.pdiparams")
rec_label_file = args.rec_label_file

# ???????????????????????????????????????????????????
# ?????????????????????????????????,???????????????
det_option, cls_option, rec_option = build_option(args)

det_model = fd.vision.ocr.DBDetector(
    det_model_file, det_params_file, runtime_option=det_option)

cls_model = fd.vision.ocr.Classifier(
    cls_model_file, cls_params_file, runtime_option=cls_option)

rec_model = fd.vision.ocr.Recognizer(
    rec_model_file, rec_params_file, rec_label_file, runtime_option=rec_option)

# ??????PP-OCR?????????3??????????????????cls_model????????????????????????????????????None
ppocr_v3 = fd.vision.ocr.PPOCRv3(
    det_model=det_model, cls_model=cls_model, rec_model=rec_model)

# ???cls???rec????????????????????????batch size
# ????????????-1, ???1????????????
# ????????????-1???, cls???rec?????????batch size????????????det????????????????????????????????????
ppocr_v3.cls_batch_size = args.cls_bs
ppocr_v3.rec_batch_size = args.rec_bs

# ??????????????????
im = cv2.imread(args.image)

#?????????????????????
result = ppocr_v3.predict(im)

print(result)

# ???????????????
vis_im = fd.vision.vis_ppocr(im, result)
cv2.imwrite("visualized_result.jpg", vis_im)
print("Visualized result save in ./visualized_result.jpg")
