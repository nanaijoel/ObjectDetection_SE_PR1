import cv2
import os
from src.ShapeAndColorDetection import process_frame
from src.logger import DataLogger
from src.visualize_shapes import visualize_shapes
from src.config_manager import load_shape_params, load_camera_params, load_color_ranges, load_config


def set_camera(camera_params):
    cap = cv2.VideoCapture(camera_params['camera_index'])
    cap.set(cv2.CAP_PROP_FPS, camera_params['fps'])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(camera_params['window_size'][0]))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(camera_params['window_size'][1]))
    return cap


def initialize_logger(config):
    log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')
    log_interval = float(config['DEFAULT']['log_interval'])
    return DataLogger(log_file, log_interval=log_interval)


def run_camera_mode():
    config = load_config(); shape_params = load_shape_params(config)
    camera_params = load_camera_params(config); color_ranges = load_color_ranges(config, 'CAMERA')

    logger = initialize_logger(config)
    cap = set_camera(camera_params)

    while True:
        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + 5)

        ret, frame = cap.read()
        if not ret:
            break
        shapes = process_frame(frame, shape_params, color_ranges)
        frame_with_shapes = visualize_shapes(frame, shapes, logger)
        cv2.imshow("Camera Feed", frame_with_shapes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def run_image_mode():
    config = load_config()
    shape_params = load_shape_params(config)
    color_ranges = load_color_ranges(config, 'IMAGE')

    logger = initialize_logger(config)

    for filename in os.listdir(config['IMAGE']['image_directory']):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(config['IMAGE']['image_directory'], filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image: {filename}")
                continue

            shapes = process_frame(image, shape_params, color_ranges)
            image_with_shapes = visualize_shapes(image, shapes, logger)
            cv2.imshow(f"Image: {filename}", image_with_shapes)
            cv2.waitKey(0)

    cv2.destroyAllWindows()
