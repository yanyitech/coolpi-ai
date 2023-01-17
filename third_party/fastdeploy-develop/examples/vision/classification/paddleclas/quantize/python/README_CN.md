[English](README.md) | 简体中文
# PaddleClas 量化模型 Python部署示例
本目录下提供的`infer.py`,可以帮助用户快速完成PaddleClas量化模型在CPU/GPU上的部署推理加速.

## 部署准备
### FastDeploy环境准备
- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. FastDeploy Python whl包安装，参考[FastDeploy Python安装](../../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

### 量化模型准备
- 1. 用户可以直接使用由FastDeploy提供的量化模型进行部署.
- 2. 用户可以使用FastDeploy提供的[一键模型自动化压缩工具](../../../../../../tools/common_tools/auto_compression/),自行进行模型量化, 并使用产出的量化模型进行部署.(注意: 推理量化后的分类模型仍然需要FP32模型文件夹下的inference_cls.yaml文件, 自行量化的模型文件夹内不包含此yaml文件, 用户从FP32模型文件夹下复制此yaml文件到量化后的模型文件夹内即可.)


## 以量化后的ResNet50_Vd模型为例, 进行部署
```bash
#下载部署示例代码
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd examples/vision/classification/paddleclas/quantize/python

#下载FastDeloy提供的ResNet50_Vd量化模型文件和测试图片
wget https://bj.bcebos.com/paddlehub/fastdeploy/resnet50_vd_ptq.tar
tar -xvf resnet50_vd_ptq.tar
wget https://gitee.com/paddlepaddle/PaddleClas/raw/release/2.4/deploy/images/ImageNet/ILSVRC2012_val_00000010.jpeg

# 在CPU上使用ONNX Runtime推理量化模型
python infer.py --model resnet50_vd_ptq --image ILSVRC2012_val_00000010.jpeg --device cpu --backend ort
# 在GPU上使用TensorRT推理量化模型
python infer.py --model resnet50_vd_ptq --image ILSVRC2012_val_00000010.jpeg --device gpu --backend trt
# 在GPU上使用Paddle-TensorRT推理量化模型
python infer.py --model resnet50_vd_ptq --image ILSVRC2012_val_00000010.jpeg --device gpu --backend pptrt
```
