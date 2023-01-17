# Do Face Recognition on Coolpi with FastDeploy

## Brief Introduction

With the improvement of AI computing power, Face Recognition algorithms have gradually shifted from machine learning to
deep learning. Through this tutorial, you will learn how to use FastDeploy to quickly implement Face Recognition on
Coolpi.

## What is ArcFace

ArcFace is a human face recognition model. Please refer
to [InsightFace Github Repo](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch) for
detailed parameters and model introduction.

## Workflow

```bash
# Download CoolPI-AI
git clone https://github.com/yanyitech/coolpi-ai.git

# Go to face detection demo
cd example/face_recognition

# Build and make
mkdir build
cd build
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/../../../third_party/fastdeploy-develop
make -j8

# 下载官方转换好的ArcFace模型文件和测试图片
wget https://bj.bcebos.com/paddlehub/fastdeploy/ms1mv3_arcface_r18.onnx
wget https://bj.bcebos.com/paddlehub/fastdeploy/rknpu2/face_demo.zip
unzip face_demo.zip

# CPU推理
./infer_arcface_demo ms1mv3_arcface_r100.onnx face_0.jpg face_1.jpg face_2.jpg 0
# RKNPU推理
./infer_arcface_demo ms1mv3_arcface_r100.onnx face_0.jpg face_1.jpg face_2.jpg 1
```

## Navigation

- [Introduction to FastDeploy](https://cool-pi.com/topic/172/coolpi-has-been-adapted-to-fastdeploy)
- [Introduction to ArcFace](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch)