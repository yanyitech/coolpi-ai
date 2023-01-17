# SCRFD C++ Deployment Example

This directory provides examples that `infer_with_scrfd.cc` fast finishes the deployment of SCRFD on NPU.

Taking the NPU inference on Linux as an example, the compilation test can be completed by executing the following
command in this directory.

```bash
mkdir build
cd build
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/../../../third_party/fastdeploy-develop
make -j8
wget https://bj.bcebos.com/paddlehub/fastdeploy/rknpu2/scrfd_500m_bnkps_shape640x640_rknpu2.zip
unzip scrfd_500m_bnkps_shape640x640_rknpu2.zip
wget https://raw.githubusercontent.com/DefTruth/lite.ai.toolkit/main/examples/lite/resources/test_lite_face_detector_3.jpg
./infer_with_scrfd scrfd_500m_bnkps_shape640x640_rknpu2/scrfd_500m_bnkps_shape640x640_rk3588_quantized.rknn \
              test_lite_face_detector_3.jpg \
              1
```

## Result

**Input picture**

![](https://user-images.githubusercontent.com/58363586/212815960-a80cb2fa-4198-4b53-a1b0-d8fda309a097.jpg)

**Output picture**

![](https://user-images.githubusercontent.com/58363586/212816086-2c59e291-2c28-4817-9ba5-1c8e18a5f8db.jpg)