# Install CoolPI-AI

Before starting your work, you need to configure the use environment of CoolPI-AI. Please enter the following command
under the CoolPI-AI root directory to complete the configuration of the environment.

```bash
source third_party/fastdeploy-develop/fastdeploy_init.sh
sudo cp third_party/fastdeploy-develop/fastdeploy_libs.conf /etc/ld.so.conf.d/
sudo ldconifg
```

Note that when you update the CoolPI-AI warehouse, you'd better execute the above command again.