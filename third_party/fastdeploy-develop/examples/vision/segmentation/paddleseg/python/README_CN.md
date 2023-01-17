[English](README.md) | 简体中文
# PaddleSeg Python部署示例

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. FastDeploy Python whl包安装，参考[FastDeploy Python安装](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

【注意】如你部署的为**PP-Matting**、**PP-HumanMatting**以及**ModNet**请参考[Matting模型部署](../../../matting)

本目录下提供`infer.py`快速完成Unet在CPU/GPU，以及GPU上通过TensorRT加速部署的示例。执行如下脚本即可完成

```bash
#下载部署示例代码
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd FastDeploy/examples/vision/segmentation/paddleseg/python

# 下载Unet模型文件和测试图片
wget https://bj.bcebos.com/paddlehub/fastdeploy/Unet_cityscapes_without_argmax_infer.tgz
tar -xvf Unet_cityscapes_without_argmax_infer.tgz
wget https://paddleseg.bj.bcebos.com/dygraph/demo/cityscapes_demo.png

# CPU推理
python infer.py --model Unet_cityscapes_without_argmax_infer --image cityscapes_demo.png --device cpu
# GPU推理
python infer.py --model Unet_cityscapes_without_argmax_infer --image cityscapes_demo.png --device gpu
# GPU上使用TensorRT推理 （注意：TensorRT推理第一次运行，有序列化模型的操作，有一定耗时，需要耐心等待）
python infer.py --model Unet_cityscapes_without_argmax_infer --image cityscapes_demo.png --device gpu --use_trt True
# 昆仑芯XPU推理
python infer.py --model Unet_cityscapes_without_argmax_infer --image cityscapes_demo.png --device kunlunxin
# 华为昇腾推理
python infer.py --model Unet_cityscapes_without_argmax_infer --image cityscapes_demo.png --device ascend
```

运行完成可视化结果如下图所示
<div  align="center">  
<img src="https://user-images.githubusercontent.com/16222477/191712880-91ae128d-247a-43e0-b1e3-cafae78431e0.jpg", width=512px, height=256px />
</div>

## PaddleSegModel Python接口

```python
fd.vision.segmentation.PaddleSegModel(model_file, params_file, config_file, runtime_option=None, model_format=ModelFormat.PADDLE)
```

PaddleSeg模型加载和初始化，其中model_file, params_file以及config_file为训练模型导出的Paddle inference文件，具体请参考其文档说明[模型导出](https://github.com/PaddlePaddle/PaddleSeg/blob/release/2.6/docs/model_export_cn.md)

**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径
> * **config_file**(str): 推理部署配置文件
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为Paddle格式

### predict函数

> ```python
> PaddleSegModel.predict(input_image)
> ```
>
> 模型预测结口，输入图像直接输出检测结果。
>
> **参数**
>
> > * **input_image**(np.ndarray): 输入数据，注意需为HWC，BGR格式

> **返回**
>
> > 返回`fastdeploy.vision.SegmentationResult`结构体，结构体说明参考文档[视觉模型预测结果](../../../../../docs/api/vision_results/)

### 类成员属性
#### 预处理参数
用户可按照自己的实际需求，修改下列预处理参数，从而影响最终的推理和部署效果

> > * **is_vertical_screen**(bool): PP-HumanSeg系列模型通过设置此参数为`true`表明输入图片是竖屏，即height大于width的图片

#### 后处理参数
> > * **apply_softmax**(bool): 当模型导出时，并未指定`apply_softmax`参数，可通过此设置此参数为`true`，将预测的输出分割标签（label_map）对应的概率结果(score_map)做softmax归一化处理

## 其它文档

- [PaddleSeg 模型介绍](..)
- [PaddleSeg C++部署](../cpp)
- [模型预测结果说明](../../../../../docs/api/vision_results/)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
