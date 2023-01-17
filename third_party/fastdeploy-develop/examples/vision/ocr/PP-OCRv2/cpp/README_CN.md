[English](README.md) | 简体中文
# PPOCRv2 C++部署示例

本目录下提供`infer.cc`快速完成PPOCRv2在CPU/GPU，以及GPU上通过TensorRT加速部署的示例。

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. 根据开发环境，下载预编译部署库和samples代码，参考[FastDeploy预编译库](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

以Linux上CPU推理为例，在本目录执行如下命令即可完成编译测试，支持此模型需保证FastDeploy版本0.7.0以上(x.x.x>=0.7.0)

```
mkdir build
cd build
# 下载FastDeploy预编译库，用户可在上文提到的`FastDeploy预编译库`中自行选择合适的版本使用
wget https://bj.bcebos.com/fastdeploy/release/cpp/fastdeploy-linux-x64-x.x.x.tgz
tar xvf fastdeploy-linux-x64-x.x.x.tgz
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/fastdeploy-linux-x64-x.x.x
make -j


# 下载模型,图片和字典文件
wget https://paddleocr.bj.bcebos.com/PP-OCRv2/chinese/ch_PP-OCRv2_det_infer.tar
tar -xvf ch_PP-OCRv2_det_infer.tar

wget https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar
tar -xvf ch_ppocr_mobile_v2.0_cls_infer.tar

wget https://paddleocr.bj.bcebos.com/PP-OCRv2/chinese/ch_PP-OCRv2_rec_infer.tar
tar -xvf ch_PP-OCRv2_rec_infer.tar

wget https://gitee.com/paddlepaddle/PaddleOCR/raw/release/2.6/doc/imgs/12.jpg

wget https://gitee.com/paddlepaddle/PaddleOCR/raw/release/2.6/ppocr/utils/ppocr_keys_v1.txt

# CPU推理
./infer_demo ./ch_PP-OCRv2_det_infer ./ch_ppocr_mobile_v2.0_cls_infer ./ch_PP-OCRv2_rec_infer ./ppocr_keys_v1.txt ./12.jpg 0
# GPU推理
./infer_demo ./ch_PP-OCRv2_det_infer ./ch_ppocr_mobile_v2.0_cls_infer ./ch_PP-OCRv2_rec_infer ./ppocr_keys_v1.txt ./12.jpg 1
# GPU上TensorRT推理
./infer_demo ./ch_PP-OCRv2_det_infer ./ch_ppocr_mobile_v2.0_cls_infer ./ch_PP-OCRv2_rec_infer ./ppocr_keys_v1.txt ./12.jpg 2
# GPU上Paddle-TRT推理
./infer_demo ./ch_PP-OCRv2_det_infer ./ch_ppocr_mobile_v2.0_cls_infer ./ch_PP-OCRv2_rec_infer ./ppocr_keys_v1.txt ./12.jpg 3
# 昆仑芯XPU推理
./infer_demo ./ch_PP-OCRv2_det_infer ./ch_ppocr_mobile_v2.0_cls_infer ./ch_PP-OCRv2_rec_infer ./ppocr_keys_v1.txt ./12.jpg 4
# 华为昇腾推理, 需要使用静态shape的demo, 若用户需要连续地预测图片, 输入图片尺寸需要准备为统一尺寸
./infer_static_shape_demo ./ch_PP-OCRv2_det_infer ./ch_ppocr_mobile_v2.0_cls_infer ./ch_PP-OCRv2_rec_infer ./ppocr_keys_v1.txt ./12.jpg 1
```

以上命令只适用于Linux或MacOS, Windows下SDK的使用方式请参考:  
- [如何在Windows中使用FastDeploy C++ SDK](../../../../../docs/cn/faq/use_sdk_on_windows.md)

如果用户使用华为昇腾NPU部署, 请参考以下方式在部署前初始化部署环境:
- [如何使用华为昇腾NPU部署](../../../../../docs/cn/faq/use_sdk_on_ascend.md)

运行完成可视化结果如下图所示

<img width="640" src="https://user-images.githubusercontent.com/109218879/185826024-f7593a0c-1bd2-4a60-b76c-15588484fa08.jpg">


## PPOCRv2 C++接口

### PPOCRv2类

```
fastdeploy::pipeline::PPOCRv2(fastdeploy::vision::ocr::DBDetector* det_model,
                fastdeploy::vision::ocr::Classifier* cls_model,
                fastdeploy::vision::ocr::Recognizer* rec_model);
```

PPOCRv2 的初始化，由检测，分类和识别模型串联构成

**参数**

> * **DBDetector**(model): OCR中的检测模型
> * **Classifier**(model): OCR中的分类模型
> * **Recognizer**(model): OCR中的识别模型

```
fastdeploy::pipeline::PPOCRv2(fastdeploy::vision::ocr::DBDetector* det_model,
                fastdeploy::vision::ocr::Recognizer* rec_model);
```
PPOCRv2 的初始化，由检测，识别模型串联构成(无分类器)

**参数**

> * **DBDetector**(model): OCR中的检测模型
> * **Recognizer**(model): OCR中的识别模型

#### Predict函数

> ```  
> bool Predict(cv::Mat* img, fastdeploy::vision::OCRResult* result);
> bool Predict(const cv::Mat& img, fastdeploy::vision::OCRResult* result);
> ```
>
> 模型预测接口，输入一张图片，返回OCR预测结果
>
> **参数**
>
> > * **img**: 输入图像，注意需为HWC，BGR格式
> > * **result**: OCR预测结果,包括由检测模型输出的检测框位置,分类模型输出的方向分类,以及识别模型输出的识别结果, OCRResult说明参考[视觉模型预测结果](../../../../../docs/api/vision_results/)


## DBDetector C++接口

### DBDetector类

```
fastdeploy::vision::ocr::DBDetector(const std::string& model_file, const std::string& params_file = "",
             const RuntimeOption& custom_option = RuntimeOption(),
             const ModelFormat& model_format = ModelFormat::PADDLE);
```

DBDetector模型加载和初始化，其中模型为paddle模型格式。

**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径，当模型格式为ONNX时，此参数传入空字符串即可
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为Paddle格式

### Classifier类与DBDetector类相同

### Recognizer类
```
  Recognizer(const std::string& model_file,
             const std::string& params_file = "",
             const std::string& label_path = "",
             const RuntimeOption& custom_option = RuntimeOption(),
             const ModelFormat& model_format = ModelFormat::PADDLE);
```
Recognizer类初始化时,需要在label_path参数中,输入识别模型所需的label文件，其他参数均与DBDetector类相同

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
- [PPOCRv2 Python部署](../python)
- [模型预测结果说明](../../../../../docs/api/vision_results/)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
