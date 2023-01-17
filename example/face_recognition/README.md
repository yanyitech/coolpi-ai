# Do Face Recognition on Coolpi with FastDeploy

## Brief Introduction

With the improvement of AI computing power, Face Recognition algorithms have gradually shifted from machine learning to deep learning. Through this tutorial, you will learn how to use FastDeploy to quickly implement Face Recognition on Coolpi.

## What is ArcFace

ArcFace is a human face recognition model. Please refer to [InsightFace Github Repo](https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch) for detailed parameters and model introduction. For developers' testing, models exported by InsightFace are provided below. Developers can download and use them directly. The accuracy metric is sourced from the model description in InsightFace. Refer to the introduction in InsightFace for more details.

|Model|Size|Accuracy (AgeDB_30)|
|-|-|-|
|[CosFace-r18](https://bj.bcebos.com/paddlehub/fastdeploy/glint360k_cosface_r18.onnx)|92MB|97.7|
|[CosFace-r34](https://bj.bcebos.com/paddlehub/fastdeploy/glint360k_cosface_r34.onnx)|131MB|98.3|
|[CosFace-r50](https://bj.bcebos.com/paddlehub/fastdeploy/glint360k_cosface_r50.onnx)|167MB|98.3|
|[CosFace-r100](https://bj.bcebos.com/paddlehub/fastdeploy/glint360k_cosface_r100.onnx)|249MB|98.4|
|[ArcFace-r18](https://bj.bcebos.com/paddlehub/fastdeploy/ms1mv3_arcface_r18.onnx)|92MB|97.7|
|[ArcFace-r34](https://bj.bcebos.com/paddlehub/fastdeploy/ms1mv3_arcface_r34.onnx)|131MB|98.1|
|[ArcFace-r50](https://bj.bcebos.com/paddlehub/fastdeploy/ms1mv3_arcface_r50.onnx)|167MB|-|
|[ArcFace-r100](https://bj.bcebos.com/paddlehub/fastdeploy/ms1mv3_arcface_r100.onnx)|249MB|98.4|
|[ArcFace-r100_lr0.1](https://bj.bcebos.com/paddlehub/fastdeploy/ms1mv3_r100_lr01.onnx)|249MB|98.4|


## How to transform the model

If you need to convert your ONNX model to RKNN model, FastDeploy also provides the corresponding method. You only need
to modify the configuration file of the model in the `tools/rknpu2/config` to achieve rapid model conversion

```Bash
git clone https://github.com/PaddlePaddle/FastDeploy.git
wget https://bj.bcebos.com/paddlehub/fastdeploy/ms1mv3_arcface_r18.onnx

python -m paddle2onnx.optimize --input_model ./ms1mv3_arcface_r18/ms1mv3_arcface_r18.onnx \
                               --output_model ./ms1mv3_arcface_r18/ms1mv3_arcface_r18.onnx \
                               --input_shape_dict "{'data':[1,3,112,112]}"
                               
python  /Path/To/FastDeploy/tools/rknpu2/export.py \
        --config_path tools/rknpu2/config/arcface_unquantized.yaml \
        --target_platform rk3588
```

## Workflow

```Bash
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