# Do Face Detection on Coolpi with FastDeploy

## Brief Introduction

With the improvement of AI computing power, Face Detection algorithms have gradually shifted from machine learning to
deep learning. Through this tutorial, you will learn how to use FastDeploy to quickly implement face detection on
Coolpi.

## What is SCRFD

SCRFD is an efficient high accuracy face detection approach which initially described
in [Arxiv](https://arxiv.org/abs/2105.04714), and accepted by ICLR-2022. In order to facilitate you to quickly
understand the parameters of the model, we only give the parameters of common models. If you need to view the detailed
data of the model, please go
to [InsightFace's official Github](https://github.com/deepinsight/insightface/tree/master/detection/scrfd).

|Name|Easy|Medium|Hard|FLOPs|Params(M)|
|-|-|-|-|-|-|
|SCRFD_500M_KPS|90.97|88.44|69.49|500M|0.57|
|SCRFD_2.5G_KPS|93.80|92.02|77.13|2.5G|0.82|
|SCRFD_10G_KPS|95.40|94.01|82.80|10G|4.23|

## Workflow

This directory provides examples that `infer_with_scrfd.cc` fast finishes the deployment of SCRFD on NPU.

Taking the NPU inference on Linux as an example, the compilation test can be completed by executing the following
command in this directory.

```bash
# Download CoolPI-AI
git clone https://github.com/yanyitech/coolpi-ai.git

# Go to face detection demo
cd example/face_detection

# Build and make
mkdir build
cd build
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/../../../third_party/fastdeploy-develop
make -j8

# Download model and picture
wget https://bj.bcebos.com/paddlehub/fastdeploy/rknpu2/scrfd_500m_bnkps_shape640x640_rknpu2.zip
unzip scrfd_500m_bnkps_shape640x640_rknpu2.zip
wget https://raw.githubusercontent.com/DefTruth/lite.ai.toolkit/main/examples/lite/resources/test_lite_face_detector_3.jpg

# Run
./infer_with_scrfd scrfd_500m_bnkps_shape640x640_rknpu2/scrfd_500m_bnkps_shape640x640_rk3588_quantized.rknn \
              test_lite_face_detector_3.jpg \
              1
```

## How to transform the model

If you need to convert your ONNX model to RKNN model, FastDeploy also provides the corresponding method. You only need
to modify the configuration file of the model in the `tools/rknpu2/config` to achieve rapid model conversion

```Bash
git clone https://github.com/PaddlePaddle/FastDeploy.git
wget  https://bj.bcebos.com/paddlehub/fastdeploy/rknpu2/scrfd_500m_bnkps_shape640x640.zip
unzip scrfd_500m_bnkps_shape640x640.zip
python  /Path/To/FastDeploy/tools/rknpu2/export.py \
        --config_path tools/rknpu2/config/scrfd_quantized.yaml \
        --target_platform rk3588

```

## Result

**Input picture**

![](https://user-images.githubusercontent.com/58363586/212815960-a80cb2fa-4198-4b53-a1b0-d8fda309a097.jpg)

**Output picture**

![](https://user-images.githubusercontent.com/58363586/212816086-2c59e291-2c28-4817-9ba5-1c8e18a5f8db.jpg)

## Navigation

- [Introduction to FastDeploy](https://cool-pi.com/topic/172/coolpi-has-been-adapted-to-fastdeploy)
- [Introduction to SCRFD](https://github.com/deepinsight/insightface/tree/master/detection/scrfd)