[English](README.md) | 简体中文
# SCRFD Python部署示例

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. FastDeploy Python whl包安装，参考[FastDeploy Python安装](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

本目录下提供`infer.py`快速完成SCRFD在CPU/GPU，以及GPU上通过TensorRT加速部署的示例。执行如下脚本即可完成

```bash
#下载部署示例代码
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd examples/vision/facedet/scrfd/python/

#下载SCRFD模型文件和测试图片
wget https://bj.bcebos.com/paddlehub/fastdeploy/scrfd_500m_bnkps_shape640x640.onnx
wget https://raw.githubusercontent.com/DefTruth/lite.ai.toolkit/main/examples/lite/resources/test_lite_face_detector_3.jpg

# CPU推理
python infer.py --model scrfd_500m_bnkps_shape640x640.onnx --image test_lite_face_detector_3.jpg --device cpu
# GPU推理
python infer.py --model scrfd_500m_bnkps_shape640x640.onnx --image test_lite_face_detector_3.jpg --device gpu
# GPU上使用TensorRT推理
python infer.py --model scrfd_500m_bnkps_shape640x640.onnx --image test_lite_face_detector_3.jpg --device gpu --use_trt True
```

运行完成可视化结果如下图所示

<img width="640" src="https://user-images.githubusercontent.com/67993288/184301789-1981d065-208f-4a6b-857c-9a0f9a63e0b1.jpg">

## SCRFD Python接口

```python
fastdeploy.vision.facedet.SCRFD(model_file, params_file=None, runtime_option=None, model_format=ModelFormat.ONNX)
```

SCRFD模型加载和初始化，其中model_file为导出的ONNX模型格式

**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径，当模型格式为ONNX格式时，此参数无需设定
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为ONNX

### predict函数

> ```python
> SCRFD.predict(image_data, conf_threshold=0.25, nms_iou_threshold=0.5)
> ```
>
> 模型预测结口，输入图像直接输出检测结果。
>
> **参数**
>
> > * **image_data**(np.ndarray): 输入数据，注意需为HWC，BGR格式
> > * **conf_threshold**(float): 检测框置信度过滤阈值
> > * **nms_iou_threshold**(float): NMS处理过程中iou阈值

> **返回**
>
> > 返回`fastdeploy.vision.FaceDetectionResult`结构体，结构体说明参考文档[视觉模型预测结果](../../../../../docs/api/vision_results/)

### 类成员属性
#### 预处理参数
用户可按照自己的实际需求，修改下列预处理参数，从而影响最终的推理和部署效果

> > * **size**(list[int]): 通过此参数修改预处理过程中resize的大小，包含两个整型元素，表示[width, height], 默认值为[640, 640]
> > * **padding_value**(list[float]): 通过此参数可以修改图片在resize时候做填充(padding)的值, 包含三个浮点型元素, 分别表示三个通道的值, 默认值为[114, 114, 114]
> > * **is_no_pad**(bool): 通过此参数让图片是否通过填充的方式进行resize, `is_no_pad=True` 表示不使用填充的方式，默认值为`is_no_pad=False`
> > * **is_mini_pad**(bool): 通过此参数可以将resize之后图像的宽高这是为最接近`size`成员变量的值, 并且满足填充的像素大小是可以被`stride`成员变量整除的。默认值为`is_mini_pad=False`
> > * **stride**(int): 配合`stris_mini_padide`成员变量使用, 默认值为`stride=32`
> > * **downsample_strides**(list[int]): 通过此参数可以修改生成anchor的特征图的下采样倍数, 包含三个整型元素, 分别表示默认的生成anchor的下采样倍数, 默认值为[8, 16, 32]
> > * **landmarks_per_face**(int): 如果使用具有人脸关键点的输出, 可以修改人脸关键点数量, 默认值为`landmarks_per_face=5`
> > * **use_kps**(bool): 通过此参数可以设置模型是否使用关键点,如果ONNX文件没有关键点输出则需要将`use_kps=False`, 并将`landmarks_per_face=0`, 默认值为`use_kps=True`
> > * **num_anchors**(int): 通过此参数可以设置每个锚点预测的anchor数量, 需要跟进训练模型的参数设定, 默认值为`num_anchors=2`


## 其它文档

- [SCRFD 模型介绍](..)
- [SCRFD C++部署](../cpp)
- [模型预测结果说明](../../../../../docs/api/vision_results/)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
