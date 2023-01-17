import fastdeploy as fd
import cv2


def parse_arguments():
    import argparse
    import ast
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", required=True, help="Path of FastestDet onnx model.")
    parser.add_argument(
        "--image", required=True, help="Path of test image file.")
    parser.add_argument(
        "--device",
        type=str,
        default='cpu',
        help="Type of inference device, support 'cpu' or 'gpu'.")
    parser.add_argument(
        "--use_trt",
        type=ast.literal_eval,
        default=False,
        help="Wether to use tensorrt.")
    return parser.parse_args()


def build_option(args):
    option = fd.RuntimeOption()

    if args.device.lower() == "gpu":
        option.use_gpu()

    if args.use_trt:
        option.use_trt_backend()
        option.set_trt_input_shape("images", [1, 3, 352, 352])
    return option


args = parse_arguments()

# Configure runtime and load model
runtime_option = build_option(args)
model = fd.vision.detection.FastestDet(args.model, runtime_option=runtime_option)

# Predict picture detection results
im = cv2.imread(args.image)
result = model.predict(im)

# Visualization of prediction results
vis_im = fd.vision.vis_detection(im, result)
cv2.imwrite("visualized_result.jpg", vis_im)
print("Visualized result save in ./visualized_result.jpg")
