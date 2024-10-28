import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QApplication

from src.camera import Camera

# noinspection PyUnresolvedReferences
class GUIMode(QMainWindow):
    def __init__(self, camera_params, detection, visualizer):
        super().__init__()
        self.camera_params = camera_params
        self.camera = Camera(camera_params)
        self.detection = detection
        self.visualizer = visualizer
        self.selected_shape = None

        # Set up video display
        self.video_label = QLabel(self)
        self.set_video_window_size(self.camera_params['window_size'])
        self.setWindowTitle("Simple GUI Mode")
        self.init_ui()

        # Start camera and frame update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)
        self.camera.initialize_camera()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)

        # Create "Triangle" filter button
        triangle_button = QPushButton("Triangle")
        triangle_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: lightgreen;
                font-weight: bold;
                border-radius: 8px;  
                border: 3px solid white;
                min-width: 100px; 
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)
        triangle_button.clicked.connect(lambda: self.set_shape_filter("Triangle"))
        layout.addWidget(triangle_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        window_width = int(self.camera_params['window_size'][0])
        window_height = int(self.camera_params['window_size'][1])
        self.setGeometry(100, 100, window_width, window_height)

    def set_shape_filter(self, shape):
        self.selected_shape = shape

    def set_video_window_size(self, window_size):
        width, height = map(int, window_size)
        self.video_label.setFixedSize(width, height)

    def update_frame(self):
        frame = self.camera.read_frame()
        if frame is not None:
            label_width = self.video_label.width()
            label_height = self.video_label.height()

            frame = cv2.resize(frame, (label_width, label_height))

            # Process frame for selected shape
            shapes = self.detection.process_frame(frame, target_shape=self.selected_shape)
            frame_with_shapes = self.visualizer.visualize_shapes(frame, shapes)

            qt_image = self.convert_cv_qt(frame_with_shapes)
            self.video_label.setPixmap(qt_image)

    @staticmethod
    def convert_cv_qt(cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        return QPixmap.fromImage(QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888))

    def closeEvent(self, event):
        self.camera.release_camera()
        event.accept()

