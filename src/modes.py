import cv2
import os
from src.ShapeAndColorDetection import ShapeAndColorDetection
from src.logger import DataLogger
from src.visualize_shapes import Visualizer
from src.config_manager import ConfigManager
from src.camera import Camera


class AppRunner:
    def __init__(self, mode):
        self.config_manager = ConfigManager()
        self.mode = mode
        self.shape_params = self.config_manager.load_shape_params()
        self.color_ranges = self.config_manager.load_color_ranges(self.mode)
        self.logger = DataLogger(self.config_manager.config, self.mode)
        self.visualizer = Visualizer()
        self.camera = None
        self.detection = ShapeAndColorDetection(self.shape_params, self.color_ranges)

    def run_camera_mode(self):
        self.camera = Camera(self.config_manager.load_camera_params())
        self.camera.initialize_camera()

        while True:
            frame = self.camera.read_frame()
            if frame is None:
                break
            shapes = self.detection.process_frame(frame)
            frame_with_shapes = self.visualizer.visualize_shapes(frame, shapes, self.logger)
            cv2.imshow("Camera Feed", frame_with_shapes)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.camera.release_camera()
        self.camera.close_window()

    def run_image_mode(self):
        for filename in os.listdir(self.config_manager.config['IMAGE']['image_directory']):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(self.config_manager.config['IMAGE']['image_directory'], filename)
                image = cv2.imread(image_path)
                if image is None:
                    print(f"Error loading image: {filename}")
                    continue

                shapes = self.detection.process_frame(image)
                image_with_shapes = self.visualizer.visualize_shapes(image, shapes, self.logger)
                cv2.imshow(f"Image: {filename}", image_with_shapes)
                cv2.waitKey(0)

        cv2.destroyAllWindows()
