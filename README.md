# CoolPI-AI

## Brief Introduction

CoolPI-AI is a free and open source repository containing a series of AI demos. Developers can quickly deploy AI models
on CoolPI with reference to demo to improve work efficiency.

## Model List

In CoolPI-AI, we provide deployment examples of the following models. We hope this will help you better use CoolPI.

|Mission Scenario|Model|Coolpi CPU / NPU speed(ms)|
|-|-|-|
|Classification|ResNet50_vd|-/33|
|Detection|Picodet|162/112|
|Detection|YOLOV5-s-relu|-/57|
|Detection|YOLOV8-n|192/119|
|Character Segmentation|PPHumanSegV2Lite-Portrait|133/43|
|Face Detection|SCRFD-2.5G-kps-640|108/42|
|Face FaceRecognition|AdaFace/ArcFace/CosFace(R18)|81/12|

## Quickly Start

Before using CoolPI-AI, you need to build a development environment. Please enter the following command in the root directory of Repo:

```bash
source third_party/fastdeploy-develop/fastdeploy_init.sh
sudo cp third_party/fastdeploy-develop/fastdeploy_libs.conf /etc/ld.so.conf.d/
sudo ldconifg
```

## Navigation

- [docs](./docs/README.md)
- [example]()
- [third party](./third_party/README.md)