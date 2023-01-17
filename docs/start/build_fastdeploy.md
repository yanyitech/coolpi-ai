# Build FastDeploy

## Brief Introduction

[FastDeploy](https://github.com/Zheng-Bicheng/FastDeploy) is an easy-to-use and high performance AI model deployment toolkit for Cloud, Mobile and Edge with out-of-the-box and unified experience, end-to-end optimization for over 150+ Text, Vision, Speech and Cross-modal AI models. Including image classification, object detection, image segmentation, face detection, face recognition, keypoint detection, matting, OCR, NLP, TTS and other tasks to meet developers' industrial deployment needs for multi-scenario, multi-hardware and multi-platform.

We spent a lot of time on the adaptation of FastDeploy for Coolpi. The model we have adapted can be used in Detection, Face Detection, Face Recognition, Face Alignment, Segmentation, OCR and other fields. These models will greatly improve Coolpi's ability in edge computing.

## How to Build FastDeploy with RKNPU2

Developers may need to compile their own FastDeploy. We provide two ways to compile FastDeploy: cross-compilation and direct board-side compilation.

If you compile directly on CoolPI, you can use ONNXRuntime and RKNPU2Runtime at the same time. If you use cross compilation, you can only use RKNPU2Runtime.

### For Direct Board-side Compilation

```bash
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd FastDeploy

# 如果您使用的是develop分支输入以下命令
git checkout develop

mkdir build && cd build
cmake ..  -DENABLE_ORT_BACKEND=ON \
	      -DENABLE_RKNPU2_BACKEND=ON \
	      -DENABLE_VISION=ON \
	      -DRKNN2_TARGET_SOC=RK3588 \
          -DCMAKE_INSTALL_PREFIX=${PWD}/fastdeploy-develop
make -j8
make install
```

### For Cross Compilation

```bash
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd FastDeploy

# 如果您使用的是develop分支输入以下命令
git checkout develop

mkdir build && cd build
cmake ..  -DCMAKE_C_COMPILER=/home/zbc/opt/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-gcc \
          -DCMAKE_CXX_COMPILER=/home/zbc/opt/gcc-linaro-6.3.1-2017.05-x86_64_aarch64-linux-gnu/bin/aarch64-linux-gnu-g++ \
          -DCMAKE_TOOLCHAIN_FILE=./../cmake/toolchain.cmake \
          -DTARGET_ABI=arm64 \
          -DENABLE_ORT_BACKEND=OFF \
	      -DENABLE_RKNPU2_BACKEND=ON \
	      -DENABLE_VISION=ON \
	      -DRKNN2_TARGET_SOC=RK3588 \
          -DCMAKE_INSTALL_PREFIX=${PWD}/fastdeploy-develop
make -j8
make install
```