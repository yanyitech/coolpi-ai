[English](README.md) | 简体中文
# YOLOv5Cls C++部署示例

本目录下提供`infer.cc`快速完成YOLOv5Cls在CPU/GPU，以及GPU上通过TensorRT加速部署的示例。

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. 根据开发环境，下载预编译部署库和samples代码，参考[FastDeploy预编译库](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

以Linux上CPU推理为例，在本目录执行如下命令即可完成编译测试，支持此模型需保证FastDeploy版本0.7.0以上(x.x.x>=0.7.0)

```bash
mkdir build
cd build
# 下载FastDeploy预编译库，用户可在上文提到的`FastDeploy预编译库`中自行选择合适的版本使用
wget https://bj.bcebos.com/fastdeploy/release/cpp/fastdeploy-linux-x64-x.x.x.tgz
tar xvf fastdeploy-linux-x64-x.x.x.tgz
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/fastdeploy-linux-x64-x.x.x
make -j

#下载官方转换好的yolov5模型文件和测试图片
wget https://bj.bcebos.com/paddlehub/fastdeploy/yolov5n-cls.onnx
wget https://gitee.com/paddlepaddle/PaddleClas/raw/release/2.4/deploy/images/ImageNet/ILSVRC2012_val_00000010.jpeg


# CPU推理
./infer_demo yolov5n-cls.onnx 000000014439.jpg 0
# GPU推理
./infer_demo yolov5n-cls.onnx 000000014439.jpg 1
# GPU上TensorRT推理
./infer_demo yolov5n-cls.onnx 000000014439.jpg 2
```

运行完成后返回结果如下所示
```bash
ClassifyResult(
label_ids: 265,
scores: 0.196327,
)
```

以上命令只适用于Linux或MacOS, Windows下SDK的使用方式请参考:  
- [如何在Windows中使用FastDeploy C++ SDK](../../../../../docs/cn/faq/use_sdk_on_windows.md)

## YOLOv5Cls C++接口

### YOLOv5Cls类

```c++
fastdeploy::vision::classification::YOLOv5Cls(
        const string& model_file,
        const string& params_file = "",
        const RuntimeOption& runtime_option = RuntimeOption(),
        const ModelFormat& model_format = ModelFormat::ONNX)
```

YOLOv5Cls模型加载和初始化，其中model_file为导出的ONNX模型格式。

**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径，当模型格式为ONNX时，此参数传入空字符串即可
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为ONNX格式

#### Predict函数

> ```c++
> YOLOv5Cls::Predict(cv::Mat* im, int topk = 1)
> ```
>
> 模型预测接口，输入图像直接输出输出分类topk结果。
>
> **参数**
>
> > * **input_image**(np.ndarray): 输入数据，注意需为HWC，BGR格式
> > * **topk**(int):返回预测概率最高的topk个分类结果，默认为1


> **返回**
>
> > 返回`fastdeploy.vision.ClassifyResult`结构体，结构体说明参考文档[视觉模型预测结果](../../../../../docs/api/vision_results/)


## 其它文档

- [YOLOv5Cls 模型介绍](..)
- [YOLOv5Cls Python部署](../python)
- [模型预测结果说明](../../../../../docs/api/vision_results/)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
