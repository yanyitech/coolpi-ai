# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import fastdeploy as fd
import cv2
import os


def parse_arguments():
    import argparse
    import ast
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_file", required=True, help="Path of FaceDet model.")
    parser.add_argument(
        "--image", type=str, required=True, help="Path of test image file.")
    return parser.parse_args()


def build_option(args):
    option = fd.RuntimeOption()
    option.use_rknpu2()
    return option


args = parse_arguments()

# 配置runtime，加载模型
runtime_option = build_option(args)
model_file = args.model_file
params_file = ""
model = fd.vision.facedet.SCRFD(
    model_file,
    params_file,
    runtime_option=runtime_option,
    model_format=fd.ModelFormat.RKNN)

model.disable_normalize()
model.disable_permute()

# 预测图片分割结果
im = cv2.imread(args.image)
result = model.predict(im)
print(result)

# 可视化结果
vis_im = fd.vision.vis_face_detection(im, result)
cv2.imwrite("visualized_result.jpg", vis_im)
print("Visualized result save in ./visualized_result.jpg")
