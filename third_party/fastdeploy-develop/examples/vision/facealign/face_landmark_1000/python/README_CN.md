[English](README.md) | 简体中文
# FaceLandmark1000 Python部署示例

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. FastDeploy Python whl包安装，参考[FastDeploy Python安装](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

本目录下提供`infer.py`快速完成FaceLandmark1000在CPU/GPU，以及GPU上通过TensorRT加速部署的示例，保证 FastDeploy 版本 >= 0.7.0 支持FaceLandmark1000模型。执行如下脚本即可完成

```bash
#下载部署示例代码
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd FastDeploy/examples/vision/facealign/facelandmark1000/python

# 下载FaceLandmark1000模型文件和测试图片
## 原版ONNX模型
wget https://bj.bcebos.com/paddlehub/fastdeploy/FaceLandmark1000.onnx
wget https://bj.bcebos.com/paddlehub/fastdeploy/facealign_input.png

# CPU推理
python infer.py --model FaceLandmark1000.onnx --image facealign_input.png --device cpu
# GPU推理
python infer.py --model FaceLandmark1000.onnx --image facealign_input.png --device gpu
# TRT推理
python infer.py --model FaceLandmark1000.onnx --image facealign_input.png --device gpu --backend trt
```

运行完成可视化结果如下图所示

<div width="500">
<img width="470" height="384" float="left" src="https://user-images.githubusercontent.com/67993288/200761309-90c096e2-c2f3-4140-8012-32ed84e5f389.jpg">
</div>

## FaceLandmark1000 Python接口

```python
fd.vision.facealign.FaceLandmark1000(model_file, params_file=None, runtime_option=None, model_format=ModelFormat.ONNX)
```

FaceLandmark1000模型加载和初始化，其中model_file为导出的ONNX模型格式

**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径，当模型格式为ONNX格式时，此参数无需设定
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为ONNX

### predict函数

> ```python
> FaceLandmark1000.predict(input_image)
> ```
>
> 模型预测结口，输入图像直接输出landmarks坐标结果。
>
> **参数**
>
> > * **input_image**(np.ndarray): 输入数据，注意需为HWC，BGR格式

> **返回**
>
> > 返回`fastdeploy.vision.FaceAlignmentResult`结构体，结构体说明参考文档[视觉模型预测结果](../../../../../docs/api/vision_results/)


## 其它文档

- [FaceLandmark1000 模型介绍](..)
- [FaceLandmark1000 C++部署](../cpp)
- [模型预测结果说明](../../../../../docs/api/vision_results/)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
