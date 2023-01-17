[English](README.md) | 简体中文
# ScaledYOLOv4准备部署模型

- ScaledYOLOv4部署实现来自[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)的代码，和[基于COCO的预训练模型](https://github.com/WongKinYiu/ScaledYOLOv4)。

  - （1）[官方库](https://github.com/WongKinYiu/ScaledYOLOv4)提供的*.pt通过[导出ONNX模型](#导出ONNX模型)操作后，可进行部署；
  - （2）自己数据训练的ScaledYOLOv4模型，按照[导出ONNX模型](#%E5%AF%BC%E5%87%BAONNX%E6%A8%A1%E5%9E%8B)操作后，参考[详细部署文档](#详细部署文档)完成部署。


## 导出ONNX模型


  访问[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)官方github库，按照指引下载安装，下载`scaledyolov4.pt` 模型，利用 `models/export.py` 得到`onnx`格式文件。如果您导出的`onnx`模型出现问题，可以参考[ScaledYOLOv4#401](https://github.com/WongKinYiu/ScaledYOLOv4/issues/401)的解决办法

  ```bash
  #下载ScaledYOLOv4模型文件
  Download from the goole drive https://drive.google.com/file/d/1aXZZE999sHMP1gev60XhNChtHPRMH3Fz/view?usp=sharing

  # 导出onnx格式文件
  python models/export.py  --weights PATH/TO/scaledyolov4-xx.pt --img-size 640
  ```


## 下载预训练ONNX模型

为了方便开发者的测试，下面提供了ScaledYOLOv4导出的各系列模型，开发者可直接下载使用。（下表中模型的精度来源于源官方库）
| 模型                                                               | 大小    | 精度    | 备注 |
|:---------------------------------------------------------------- |:----- |:----- |:----- |
| [ScaledYOLOv4-P5-896](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p5-896.onnx) | 271MB | 51.2% | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P5+BoF-896](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p5_-896.onnx) | 271MB | 51.7% | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P6-1280](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p6-1280.onnx) | 487MB | 53.9% | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P6+BoF-1280](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p6_-1280.onnx) | 487MB | 54.4% | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P7-1536](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p7-1536.onnx) | 1.1GB | 55.0% | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P5](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p5.onnx) | 271MB | - | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P5+BoF](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p5_.onnx) | 271MB | -| 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P6](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p6.onnx) | 487MB | - | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P6+BoF](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p6_.onnx) | 487MB | - | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |
| [ScaledYOLOv4-P7](https://bj.bcebos.com/paddlehub/fastdeploy/scaled_yolov4-p7.onnx) | 1.1GB | - | 此模型文件来源于[ScaledYOLOv4](https://github.com/WongKinYiu/ScaledYOLOv4)，GPL-3.0 License |


## 详细部署文档

- [Python部署](python)
- [C++部署](cpp)


## 版本说明

- 本版本文档和代码基于[ScaledYOLOv4 CommitID: 6768003](https://github.com/WongKinYiu/ScaledYOLOv4/commit/676800364a3446900b9e8407bc880ea2127b3415) 编写
