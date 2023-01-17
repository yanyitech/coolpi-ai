[English](README.md) | 简体中文
# BasicVSR C++部署示例

本目录下提供`infer.cc`快速完成BasicVSR在CPU/GPU，以及GPU上通过TensorRT加速部署的示例。

在部署前，需确认以下两个步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)
- 2. 根据开发环境，下载预编译部署库和samples代码，参考[FastDeploy预编译库](../../../../../docs/cn/build_and_install/download_prebuilt_libraries.md)
以Linux上BasicVSR推理为例，在本目录执行如下命令即可完成编译测试，支持此模型需保证FastDeploy版本0.7.0以上(x.x.x>=0.7.0)

```bash
mkdir build
cd build
# 下载FastDeploy预编译库，用户可在上文提到的`FastDeploy预编译库`中自行选择合适的版本使用
wget https://bj.bcebos.com/fastdeploy/release/cpp/fastdeploy-linux-x64-x.x.x.tgz
tar xvf fastdeploy-linux-x64-x.x.x.tgz
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/fastdeploy-linux-x64-x.x.x
make -j

# 下载BasicVSR模型文件和测试视频
wget https://bj.bcebos.com/paddlehub/fastdeploy/BasicVSR_reds_x4.tar
tar -xvf BasicVSR_reds_x4.tar
wget https://bj.bcebos.com/paddlehub/fastdeploy/vsr_src.mp4


# CPU推理
./infer_demo BasicVSR_reds_x4 vsr_src.mp4 0 2
# GPU推理
./infer_demo BasicVSR_reds_x4 vsr_src.mp4 1 2
# GPU上TensorRT推理
./infer_demo BasicVSR_reds_x4 vsr_src.mp4 2 2
```

以上命令只适用于Linux或MacOS, Windows下SDK的使用方式请参考:  
- [如何在Windows中使用FastDeploy C++ SDK](../../../../../docs/cn/faq/use_sdk_on_windows.md)

## BasicVSR C++接口

### BasicVSR类

```c++
fastdeploy::vision::sr::BasicVSR(
        const string& model_file,
        const string& params_file = "",
        const RuntimeOption& runtime_option = RuntimeOption(),
        const ModelFormat& model_format = ModelFormat::PADDLE)
```

BasicVSR模型加载和初始化，其中model_file为导出的Paddle模型格式。

**参数**

> * **model_file**(str): 模型文件路径
> * **params_file**(str): 参数文件路径
> * **runtime_option**(RuntimeOption): 后端推理配置，默认为None，即采用默认配置
> * **model_format**(ModelFormat): 模型格式，默认为Paddle格式

#### Predict函数

> ```c++
> BasicVSR::Predict(std::vector<cv::Mat>& imgs, std::vector<cv::Mat>& results)
> ```
>
> 模型预测接口，输入图像直接输出检测结果。
>
> **参数**
>
> > * **imgs**: 输入视频帧序列，注意需为HWC，BGR格式
> > * **results**: 视频超分结果，超分后的视频帧序列

- [模型介绍](../../)
- [Python部署](../python)
- [如何切换模型推理后端引擎](../../../../../docs/cn/faq/how_to_change_backend.md)
