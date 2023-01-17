[English](README.md) | 简体中文
# RobustVideoMatting 模型部署

## 模型版本说明

- [RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting/commit/81a1093)

## 支持模型列表

目前FastDeploy支持如下模型的部署

- [RobustVideoMatting 模型](https://github.com/PeterL1n/RobustVideoMatting)

## 下载预训练模型

为了方便开发者的测试，下面提供了RobustVideoMatting导出的各系列模型，开发者可直接下载使用。

| 模型                                                               | 参数大小    | 精度    | 备注 |
|:---------------------------------------------------------------- |:----- |:----- | :------ |
| [rvm_mobilenetv3_fp32.onnx](https://bj.bcebos.com/paddlehub/fastdeploy/rvm_mobilenetv3_fp32.onnx) | 15MB ||exported from [RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting/commit/81a1093)，GPL-3.0 License |
| [rvm_resnet50_fp32.onnx](https://bj.bcebos.com/paddlehub/fastdeploy/rvm_resnet50_fp32.onnx) | 103MB | |exported from [RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting/commit/81a1093)，GPL-3.0 License |
| [rvm_mobilenetv3_trt.onnx](https://bj.bcebos.com/paddlehub/fastdeploy/rvm_mobilenetv3_trt.onnx) | 15MB | |exported from [RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting/commit/81a1093)，GPL-3.0 License |
| [rvm_resnet50_trt.onnx](https://bj.bcebos.com/paddlehub/fastdeploy/rvm_resnet50_trt.onnx) | 103MB | | exported from [RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting/commit/81a1093)，GPL-3.0 License |

**Note**：
- 如果要使用 TensorRT 进行推理，需要下载后缀为 trt 的 onnx 模型文件

## 详细部署文档

- [Python部署](python)
- [C++部署](cpp)
