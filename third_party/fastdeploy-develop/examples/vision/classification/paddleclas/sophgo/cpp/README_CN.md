[English](README.md) | 简体中文
# PaddleClas C++部署示例

本目录下提供`infer.cc`快速完成ResNet50_vd模型在SOPHGO BM1684x板子上加速部署的示例。

在部署前，需确认以下两个步骤:

1. 软硬件环境满足要求
2. 根据开发环境，从头编译FastDeploy仓库

以上步骤请参考[SOPHGO部署库编译](../../../../../../docs/cn/build_and_install/sophgo.md)实现

## 生成基本目录文件

该例程由以下几个部分组成
```text
.
├── CMakeLists.txt
├── build  # 编译文件夹
├── image  # 存放图片的文件夹
├── infer.cc
├── preprocess_config.yaml #示例前处理配置文件
└── model  # 存放模型文件的文件夹
```

## 编译

### 编译并拷贝SDK到thirdpartys文件夹

请参考[SOPHGO部署库编译](../../../../../../docs/cn/build_and_install/sophgo.md)仓库编译SDK，编译完成后，将在build目录下生成fastdeploy-0.0.3目录.

### 拷贝模型文件，以及配置文件至model文件夹
将Paddle模型转换为SOPHGO bmodel模型，转换步骤参考[文档](../README.md)  
将转换后的SOPHGO bmodel模型文件拷贝至model中  
将前处理配置文件也拷贝到model中  
```bash
cp preprocess_config.yaml ./model
```

### 准备测试图片至image文件夹
```bash
wget https://gitee.com/paddlepaddle/PaddleClas/raw/release/2.4/deploy/images/ImageNet/ILSVRC2012_val_00000010.jpeg
cp ILSVRC2012_val_00000010.jpeg ./images
```

### 编译example

```bash
cd build
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/fastdeploy-0.0.3
make
```

## 运行例程

```bash
./infer_demo model images/ILSVRC2012_val_00000010.jpeg
```


- [模型介绍](../../)
- [模型转换](../)
