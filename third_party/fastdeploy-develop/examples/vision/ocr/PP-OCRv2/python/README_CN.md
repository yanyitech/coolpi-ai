[English](README.md) | 简体中文
# PPOCRv2 Python部署示例

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. FastDeploy Python whl包安装，参考[FastDeploy Python安装](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

本目录下提供`infer.py`快速完成PPOCRv2在CPU/GPU，以及GPU上通过TensorRT加速部署的示例。执行如下脚本即可完成

```

# 下载模型,图片和字典文件
wget https://paddleocr.bj.bcebos.com/PP-OCRv2/chinese/ch_PP-OCRv2_det_infer.tar
tar -xvf ch_PP-OCRv2_det_infer.tar

wget https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar
tar -xvf ch_ppocr_mobile_v2.0_cls_infer.tar

wget https://paddleocr.bj.bcebos.com/PP-OCRv2/chinese/ch_PP-OCRv2_rec_infer.tar
tar -xvf ch_PP-OCRv2_rec_infer.tar

wget https://gitee.com/paddlepaddle/PaddleOCR/raw/release/2.6/doc/imgs/12.jpg

wget https://gitee.com/paddlepaddle/PaddleOCR/raw/release/2.6/ppocr/utils/ppocr_keys_v1.txt


#下载部署示例代码
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd examples/vison/ocr/PP-OCRv2/python/

# CPU推理
python infer.py --det_model ch_PP-OCRv2_det_infer --cls_model ch_ppocr_mobile_v2.0_cls_infer --rec_model ch_PP-OCRv2_rec_infer --rec_label_file ppocr_keys_v1.txt --image 12.jpg --device cpu
# GPU推理
python infer.py --det_model ch_PP-OCRv2_det_infer --cls_model ch_ppocr_mobile_v2.0_cls_infer --rec_model ch_PP-OCRv2_rec_infer --rec_label_file ppocr_keys_v1.txt --image 12.jpg --device gpu
# GPU上使用TensorRT推理
python infer.py --det_model ch_PP-OCRv2_det_infer --cls_model ch_ppocr_mobile_v2.0_cls_infer --rec_model ch_PP-OCRv2_rec_infer --rec_label_file ppocr_keys_v1.txt --image 12.jpg --device gpu --backend trt
# 昆仑芯XPU推理
python infer.py --det_model ch_PP-OCRv2_det_infer --cls_model ch_ppocr_mobile_v2.0_cls_infer --rec_model ch_PP-OCRv2_rec_infer --rec_label_file ppocr_keys_v1.txt --image 12.jpg --device kunlunxin
# 华为昇腾推理,需要使用静态shape脚本, 若用户需要连续地预测图片, 输入图片尺寸需要准备为统一尺寸
python infer_static_shape.py --det_model ch_PP-OCRv2_det_infer --cls_model ch_ppocr_mobile_v2.0_cls_infer --rec_model ch_PP-OCRv2_rec_infer --rec_label_file ppocr_keys_v1.txt --image 12.jpg --device ascend
```

运行完成可视化结果如下图所示
<img width="640" src="https://user-images.githubusercontent.com/109218879/185826024-f7593a0c-1bd2-4a60-b76c-15588484fa08.jpg">

## PPOCRv2 Python接口

```
fd.vision.ocr.PPOCRv2(det_model=det_model, cls_model=cls_model, rec_model=rec_model)
```
PPOCRv2的初始化,输入的参数是检测模型，分类模型和识别模型，其中cls_model可选，如无需求，可设置为None

**参数**

> * **det_model**(model): OCR中的检测模型
> * **cls_model**(model): OCR中的分类模型
> * **rec_model**(model): OCR中的识别模型

### predict函数

> ```
> result = ppocr_v2.predict(im)
> ```
>
> 模型预测接口，输入是一张图片
>
> **参数**
>
> > * **im**(np.ndarray): 输入数据，每张图片注意需为HWC，BGR格式

> **返回**
>
> > 返回`fastdeploy.vision.OCRResult`结构体，结构体说明参考文档[视觉模型预测结果](../../../../../docs/api/vision_results/)



## DBDetector Python接口

### DBDetector类

```
fastdeploy.vision.ocr.DBDetector(model_file, params_file, runtime_option=None, model_format=ModelFormat.PADDLE)
```

DBDetector模型加载和初始化，其中模型为paddle模型格式。

**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径，当模型格式为ONNX时，此参数传入空字符串即可
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为PADDLE格式

### Classifier类与DBDetector类相同

### Recognizer类
```
fastdeploy.vision.ocr.Recognizer(rec_model_file,rec_params_file,rec_label_file,
                                  runtime_option=rec_runtime_option,model_format=ModelFormat.PADDLE)
```
Recognizer类初始化时,需要在rec_label_file参数中,输入识别模型所需的label文件路径，其他参数均与DBDetector类相同

**参数**
> * **label_path**(str): 识别模型的label文件路径



### 类成员变量

#### DBDetector预处理参数
用户可按照自己的实际需求，修改下列预处理参数，从而影响最终的推理和部署效果

> > * **max_side_len**(int): 检测算法前向时图片长边的最大尺寸，当长边超出这个值时会将长边resize到这个大小，短边等比例缩放,默认为960
> > * **det_db_thresh**(double): DB模型输出预测图的二值化阈值，默认为0.3
> > * **det_db_box_thresh**(double): DB模型输出框的阈值，低于此值的预测框会被丢弃，默认为0.6
> > * **det_db_unclip_ratio**(double): DB模型输出框扩大的比例，默认为1.5
> > * **det_db_score_mode**(string):DB后处理中计算文本框平均得分的方式,默认为slow，即求polygon区域的平均分数的方式
> > * **use_dilation**(bool):是否对检测输出的feature map做膨胀处理,默认为Fasle

#### Classifier预处理参数
用户可按照自己的实际需求，修改下列预处理参数，从而影响最终的推理和部署效果

> > * **cls_thresh**(double): 当分类模型输出的得分超过此阈值，输入的图片将被翻转，默认为0.9



## 其它文档

- [PPOCR 系列模型介绍](../../)
- [PPOCRv2 C++部署](../cpp)
- [模型预测结果说明](../../../../../docs/api/vision_results/)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
