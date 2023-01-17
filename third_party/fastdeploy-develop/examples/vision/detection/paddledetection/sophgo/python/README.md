# PaddleDetection Python部署示例

在部署前，需确认以下步骤

- 1. 软硬件环境满足要求，参考[FastDeploy环境要求](../../../../../../docs/cn/build_and_install/sophgo.md)

本目录下提供`infer_ppyoloe.py`和`infer_picodet.py`快速完成 PP-YOLOE 和 PicoDet 在SOPHGO TPU上部署的示例。执行如下脚本即可完成

```bash
# 下载部署示例代码
git clone https://github.com/PaddlePaddle/FastDeploy.git
cd FastDeploy/examples/vision/detection/paddledetection/sophgo/python

# 下载图片
wget https://gitee.com/paddlepaddle/PaddleDetection/raw/release/2.4/demo/000000014439.jpg

# 推理
#ppyoloe推理示例
python3 infer_ppyoloe.py --model_file model/ppyoloe_crn_s_300e_coco_1684x_f32.bmodel --config_file model/infer_cfg.yml --image ./000000014439.jpg

#picodet推理示例
python3 infer_picodet.py --model_file model/picodet_s_416_coco_lcnet_1684x_f32.bmodel --config_file model/infer_cfg.yml --image ./000000014439.jpg

# 运行完成后返回结果如下所示
可视化结果存储在sophgo_result.jpg中
```

## 其它文档
- [PP-YOLOE C++部署](../cpp)
- [PicoDet C++部署](../cpp)
- [转换PicoDet SOPHGO模型文档](../README.md)
- [转换PP-YOLOE SOPHGO模型文档](../README.md)
