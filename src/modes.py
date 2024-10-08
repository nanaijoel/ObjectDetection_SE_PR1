import cv2
import os
from src.ShapeAndColorDetection import process_frame
from src.logger import DataLogger
from src.visualize_shapes import visualize_shapes


def run_camera_mode(config):
    camera_index = int(config['CAMERA']['camera_index']); window_size = config['CAMERA']['window_size'].split('x')
    fps = int(config['CAMERA']['fps']); log_interval = float(config['DEFAULT']['log_interval'])
    log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')

    logger = DataLogger(log_file, log_interval=log_interval)

    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(window_size[0])); cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(window_size[1]))
    cap.set(cv2.CAP_PROP_FPS, fps)

    frame_count = 0; process_interval = 5  # Process every fifth frame

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % process_interval == 0:  # Only process every fifth frame
            shapes = process_frame(frame, config, mode='CAMERA')
            frame_with_shapes = visualize_shapes(frame, shapes, logger)
            cv2.imshow("Camera Feed", frame_with_shapes)
        frame_count = (frame_count + 1) % process_interval  # Reset counter after reaching process_interval
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




def run_image_mode(config):
    image_directory = config['IMAGE']['image_directory']
    log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')

    logger = DataLogger(log_file)

    for filename in os.listdir(image_directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_directory, filename)
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error loading image: {filename}")
                continue
            shapes = process_frame(image, config, mode='IMAGE')
            image_with_shapes = visualize_shapes(image, shapes, logger)
            cv2.imshow(f"Image: {filename}", image_with_shapes)
            cv2.waitKey(0)

    cv2.destroyAllWindows()
