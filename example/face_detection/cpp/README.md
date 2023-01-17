```bash
mkdir build
cd build
# 下载FastDeploy预编译库，用户可在上文提到的`FastDeploy预编译库`中自行选择合适的版本使用
wget https://bj.bcebos.com/fastdeploy/release/cpp/fastdeploy-linux-aarch64-rk356X-x.x.x.tgz
tar -xzvf fastdeploy-linux-aarch64-rk356X-x.x.x.tgz
cmake .. -DFASTDEPLOY_INSTALL_DIR=${PWD}/fastdeploy-linux-aarch64-rk356X
make -j8
#下载官方转换好的SCRFD模型文件和测试图片
wget https://bj.bcebos.com/paddlehub/fastdeploy/rknpu2/scrfd_500m_bnkps_shape640x640_rknpu2.zip
unzip scrfd_500m_bnkps_shape640x640_rknpu2.zip
wget https://raw.githubusercontent.com/DefTruth/lite.ai.toolkit/main/examples/lite/resources/test_lite_face_detector_3.jpg
./infer_demo scrfd_500m_bnkps_shape640x640_rknpu2/scrfd_500m_bnkps_shape640x640_rk3568_quantized.rknn \
              test_lite_face_detector_3.jpg \
              1
```