[English](README.md) | 简体中文
# YOLOv7End2EndORT Python部署示例

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. FastDeploy Python whl包安装，参考[FastDeploy Python安装](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

本目录下提供`infer.py`快速完成YOLOv7End2End在CPU/GPU部署的示例。执行如下脚本即可完成

```bash
#下载部署示例代码
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd FastDeploy/examples/vision/detection/yolov7end2end_ort/python/
# 如果预编译的Python wheel包还没有支持该模型，请从develop分支源码编译最新python包进行安装

#下载yolov7模型文件和测试图片
wget https://bj.bcebos.com/paddlehub/fastdeploy/yolov7-end2end-ort-nms.onnx
wget https://gitee.com/paddlepaddle/PaddleDetection/raw/release/2.4/demo/000000014439.jpg

# CPU推理
python infer.py --model yolov7-end2end-ort-nms.onnx --image 000000014439.jpg --device cpu
# GPU推理
python infer.py --model yolov7-end2end-ort-nms.onnx --image 000000014439.jpg --device gpu
# TensorRT + GPU推理 (暂不支持 会回退到 ORT + GPU)
python infer.py --model yolov7-end2end-ort-nms.onnx --image 000000014439.jpg --device gpu --use_trt True
```

运行完成可视化结果如下图所示

<div align='center'>
  <img width="639" alt="image" src="https://user-images.githubusercontent.com/31974251/186369053-1b578d61-ca70-4755-9671-c9fccf6314a0.png">
</div>

注意，YOLOv7End2EndORT是专门用于推理YOLOv7中导出模型带[ORT_NMS](https://github.com/WongKinYiu/yolov7/blob/main/models/experimental.py#L87) 版本的End2End模型，不带nms的模型推理请使用YOLOv7类，而 [TRT_NMS](https://github.com/WongKinYiu/yolov7/blob/main/models/experimental.py#L111) 版本的End2End模型请使用YOLOv7End2EndTRT进行推理。

## YOLOv7End2EndORT Python接口

```python
fastdeploy.vision.detection.YOLOv7End2EndORT(model_file, params_file=None, runtime_option=None, model_format=ModelFormat.ONNX)
```

YOLOv7End2EndORT模型加载和初始化，其中model_file为导出的ONNX模型格式

**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径，当模型格式为ONNX格式时，此参数无需设定
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为ONNX

### predict函数

> ```python
> YOLOv7End2EndORT.predict(image_data, conf_threshold=0.25)
> ```
>
> 模型预测结口，输入图像直接输出检测结果。
>
> **参数**
>
> > * **image_data**(np.ndarray): 输入数据，注意需为HWC，BGR格式
> > * **conf_threshold**(float): 检测框置信度过滤阈值，但由于YOLOv7 End2End的模型在导出成ONNX时已经指定了score阈值，因此该参数只有在大于已经指定的阈值时才会有效。

> **返回**
>
> > 返回`fastdeploy.vision.DetectionResult`结构体，结构体说明参考文档[视觉模型预测结果](../../../../../docs/api/vision_results/)

### 类成员属性
#### 预处理参数
用户可按照自己的实际需求，修改下列预处理参数，从而影响最终的推理和部署效果

> > * **size**(list[int]): 通过此参数修改预处理过程中resize的大小，包含两个整型元素，表示[width, height], 默认值为[640, 640]
> > * **padding_value**(list[float]): 通过此参数可以修改图片在resize时候做填充(padding)的值, 包含三个浮点型元素, 分别表示三个通道的值, 默认值为[114, 114, 114]
> > * **is_no_pad**(bool): 通过此参数让图片是否通过填充的方式进行resize, `is_no_pad=True` 表示不使用填充的方式，默认值为`is_no_pad=False`
> > * **is_mini_pad**(bool): 通过此参数可以将resize之后图像的宽高这是为最接近`size`成员变量的值, 并且满足填充的像素大小是可以被`stride`成员变量整除的。默认值为`is_mini_pad=False`
> > * **stride**(int): 配合`stris_mini_padide`成员变量使用, 默认值为`stride=32`



## 其它文档

- [YOLOv7End2EndORT 模型介绍](..)
- [YOLOv7End2EndORT C++部署](../cpp)
- [模型预测结果说明](../../../../../docs/api/vision_results/)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
