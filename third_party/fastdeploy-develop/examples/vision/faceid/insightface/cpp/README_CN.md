[English](README.md) | 简体中文
# InsightFace C++部署示例
本目录下提供infer_xxx.cc快速完成InsighFace模型包括ArcFace\CosFace\VPL\Partial_FC在CPU/GPU，以及GPU上通过TensorRT加速部署的示例。
以ArcFace为例提供`infer_arcface.cc`快速完成ArcFace在CPU/GPU，以及GPU上通过TensorRT加速部署的示例。

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)  
- 2. 根据开发环境，下载预编译部署库和samples代码，参考[FastDeploy预编译库](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)

以Linux上CPU推理为例，在本目录执行如下命令即可完成编译测试

```bash
mkdir build
cd build
wget https://bj.bcebos.com/fastdeploy/release/cpp/fastdeploy-linux-x64-x.x.x.tgz
tar xvf fastdeploy-linux-x64-x.x.x.tgz
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/fastdeploy-linux-x64-x.x.x
make -j

#下载官方转换好的ArcFace模型文件和测试图片
wget https://bj.bcebos.com/paddlehub/fastdeploy/ms1mv3_arcface_r100.onnx
wget https://bj.bcebos.com/paddlehub/fastdeploy/rknpu2/face_demo.zip
unzip face_demo.zip

# CPU推理
./infer_arcface_demo ms1mv3_arcface_r100.onnx face_0.jpg face_1.jpg face_2.jpg 0
# GPU推理
./infer_arcface_demo ms1mv3_arcface_r100.onnx face_0.jpg face_1.jpg face_2.jpg 1
# GPU上TensorRT推理
./infer_arcface_demo ms1mv3_arcface_r100.onnx face_0.jpg face_1.jpg face_2.jpg 2
```

运行完成可视化结果如下图所示

<div width="700">
<img width="220" float="left" src="https://user-images.githubusercontent.com/67993288/184321537-860bf857-0101-4e92-a74c-48e8658d838c.JPG">
<img width="220" float="left" src="https://user-images.githubusercontent.com/67993288/184322004-a551e6e4-6f47-454e-95d6-f8ba2f47b516.JPG">
<img width="220" float="left" src="https://user-images.githubusercontent.com/67993288/184321622-d9a494c3-72f3-47f1-97c5-8a2372de491f.JPG">
</div>

以上命令只适用于Linux或MacOS, Windows下SDK的使用方式请参考:  
- [如何在Windows中使用FastDeploy C++ SDK](../../../../../docs/cn/faq/use_sdk_on_windows.md)

## InsightFace C++接口

### ArcFace类

```c++
fastdeploy::vision::faceid::ArcFace(
        const string& model_file,
        const string& params_file = "",
        const RuntimeOption& runtime_option = RuntimeOption(),
        const ModelFormat& model_format = ModelFormat::ONNX)
```

ArcFace模型加载和初始化，其中model_file为导出的ONNX模型格式。

### CosFace类

```c++
fastdeploy::vision::faceid::CosFace(
        const string& model_file,
        const string& params_file = "",
        const RuntimeOption& runtime_option = RuntimeOption(),
        const ModelFormat& model_format = ModelFormat::ONNX)
```

CosFace模型加载和初始化，其中model_file为导出的ONNX模型格式。

### PartialFC类

```c++
fastdeploy::vision::faceid::PartialFC(
        const string& model_file,
        const string& params_file = "",
        const RuntimeOption& runtime_option = RuntimeOption(),
        const ModelFormat& model_format = ModelFormat::ONNX)
```

PartialFC模型加载和初始化，其中model_file为导出的ONNX模型格式。

### VPL类

```c++
fastdeploy::vision::faceid::VPL(
        const string& model_file,
        const string& params_file = "",
        const RuntimeOption& runtime_option = RuntimeOption(),
        const ModelFormat& model_format = ModelFormat::ONNX)
```

VPL模型加载和初始化，其中model_file为导出的ONNX模型格式。
**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径，当模型格式为ONNX时，此参数传入空字符串即可
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为ONNX格式

#### Predict函数

> ```c++
> ArcFace::Predict(const cv::Mat& im, FaceRecognitionResult* result)
> ```
>
> 模型预测接口，输入图像直接输出检测结果。
>
> **参数**
>
> > * **im**: 输入图像，注意需为HWC，BGR格式
> > * **result**: 检测结果，包括检测框，各个框的置信度, FaceRecognitionResult说明参考[视觉模型预测结果](../../../../../docs/api/vision_results/)

### 修改预处理以及后处理的参数
预处理和后处理的参数的需要通过修改InsightFaceRecognitionPostprocessor，InsightFaceRecognitionPreprocessor的成员变量来进行修改。

#### InsightFaceRecognitionPreprocessor成员变量(预处理参数)
> > * **size**(vector&lt;int&gt;): 通过此参数修改预处理过程中resize的大小，包含两个整型元素，表示[width, height], 默认值为[112, 112],
      通过InsightFaceRecognitionPreprocessor::SetSize(std::vector<int>& size)来进行修改
> > * **alpha**(vector&lt;float&gt;): 预处理归一化的alpha值，计算公式为`x'=x*alpha+beta`，alpha默认为[1. / 127.5, 1.f / 127.5, 1. / 127.5],
      通过InsightFaceRecognitionPreprocessor::SetAlpha(std::vector<float>& alpha)来进行修改
> > * **beta**(vector&lt;float&gt;): 预处理归一化的beta值，计算公式为`x'=x*alpha+beta`，beta默认为[-1.f, -1.f, -1.f],
      通过InsightFaceRecognitionPreprocessor::SetBeta(std::vector<float>& beta)来进行修改

#### InsightFaceRecognitionPostprocessor成员变量(后处理参数)
> > * **l2_normalize**(bool): 输出人脸向量之前是否执行l2归一化，默认false,
      InsightFaceRecognitionPostprocessor::SetL2Normalize(bool& l2_normalize)来进行修改

- [模型介绍](../../)
- [Python部署](../python)
- [视觉模型预测结果](../../../../../docs/api/vision_results/)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
