English | [简体中文](README_CN.md)
# YOLOv7End2EndORT Python Deployment Example

Two steps before deployment

- 1. Software and hardware should meet the requirements. Please refer to [FastDeploy Environment Requirements](../../../../../docs/en/build_and_install/download_prebuilt_libraries.md)  
- 2. Install FastDeploy Python whl package. Refer to [FastDeploy Python Installation](../../../../../docs/en/build_and_install/download_prebuilt_libraries.md)

This directory provides examples that `infer.py` fast finishes the deployment of YOLOv7End2End on CPU/GPU accelerated by TensorRT. The script is as follows

```bash
# Download the example code for deployment
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd FastDeploy/examples/vision/detection/yolov7end2end_ort/python/
# If the precompiled Python wheel package does not support the model, compile the latest python package from the source code of develop branch and install it.

# Download yolov7 model files and test images
wget https://bj.bcebos.com/paddlehub/fastdeploy/yolov7-end2end-ort-nms.onnx
wget https://gitee.com/paddlepaddle/PaddleDetection/raw/release/2.4/demo/000000014439.jpg

# CPU inference
python infer.py --model yolov7-end2end-ort-nms.onnx --image 000000014439.jpg --device cpu
# GPU inference
python infer.py --model yolov7-end2end-ort-nms.onnx --image 000000014439.jpg --device gpu
# TensorRT + GPU inference (Not supported yet. Back to ORT + GPU)
python infer.py --model yolov7-end2end-ort-nms.onnx --image 000000014439.jpg --device gpu --use_trt True
```

The visualized result after running is as follows

<div align='center'>
  <img width="639" alt="image" src="https://user-images.githubusercontent.com/31974251/186369053-1b578d61-ca70-4755-9671-c9fccf6314a0.png">
</div>

Attention: YOLOv7End2EndORT is designed for the inference of End2End models with [ORT_NMS](https://github.com/WongKinYiu/yolov7/blob/main/models/experimental.py#L87) among the YOLOv7 exported models. For models without nms, use YOLOv7 class for inference. For End2End models with [TRT_NMS](https://github.com/WongKinYiu/yolov7/blob/main/models/experimental.py#L111), use YOLOv7End2EndTRT for inference.

## YOLOv7End2EndORT Python Interface 

```python
fastdeploy.vision.detection.YOLOv7End2EndORT(model_file, params_file=None, runtime_option=None, model_format=ModelFormat.ONNX)
```

YOLOv7End2EndORT model loading and initialization, among which model_file is the exported ONNX model format

**Parameter**

> * **model_file**(str): Model file path 
> * **params_file**(str): Parameter file path. No need to set when the model is in ONNX format
> * **runtime_option**(RuntimeOption): Backend inference configuration. None by default, which is the default configuration
> * **model_format**(ModelFormat): Model format. ONNX format by default

### predict function

> ```python
> YOLOv7End2EndORT.predict(image_data, conf_threshold=0.25)
> ```
>
> Model prediction interface. Input images and output detection results.
>
> **Parameter**
>
> > * **image_data**(np.ndarray): Input data in HWC or BGR format
> > * **conf_threshold**(float): Filtering threshold of detection box confidence. But considering that YOLOv7 End2End models have a score threshold specified during ONNX export, this parameter will be effective when being greater than the specified one.

> **Return**
>
> > Return `fastdeploy.vision.DetectionResult` structure. Refer to [Vision Model Prediction Results](../../../../../docs/api/vision_results/) for its description.

### Class Member Property
#### Pre-processing Parameter
Users can modify the following pre-processing parameters to their needs, which affects the final inference and deployment results

> > * **size**(list[int]): This parameter changes resize used during preprocessing, containing two integer elements for [width, height]  with default value [640, 640]
> > * **padding_value**(list[float]): This parameter is used to change the padding value of images during resize, containing three floating-point elements that represent the value of three channels. Default value [114, 114, 114]
> > * **is_no_pad**(bool): Specify whether to resize the image through padding. `is_no_pad=True` represents no paddling. Default `is_no_pad=False`
> > * **is_mini_pad**(bool): This parameter sets the width and height of the image after resize to the value nearest to the `size` member variable and to the point where the padded pixel size is divisible by the `stride`  member variable. Default `is_mini_pad=False`
> > * **stride**(int): Used with the `stris_mini_padide` member variable. Default `stride=32`



## Other Documents

- [YOLOv7End2EndORT Model Description](..)
- [YOLOv7End2EndORT C++ Deployment](../cpp)
- [Model Prediction Results](../../../../../docs/api/vision_results/)
- [How to switch the model inference backend engine](../../../../../docs/en/faq/how_to_change_backend.md)
