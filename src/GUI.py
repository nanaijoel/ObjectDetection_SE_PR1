# GUI which allows to filter the detected shapes on one specific shape

import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDockWidget, QMenuBar, \
    QAction, QMessageBox

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
        self.video_label = QLabel(self)
        self.set_video_window_size(self.camera_params['window_size'])
        self.setWindowTitle("GUI Mode")
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.camera.initialize_camera()


    def create_buttons(self):
        self.create_menu()
        dock_widget = self.create_dock_widget()
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

    def create_menu(self):
        menu_bar = QMenuBar(self)
        info_menu = menu_bar.addMenu("Info")

        info_action = QAction("Show Info", self)
        info_action.triggered.connect(self.show_info_popup)
        info_menu.addAction(info_action)

        self.setMenuBar(menu_bar)

    def create_dock_widget(self):
        button_layout = QVBoxLayout()

        for btn in self.create_shape_buttons():
            button_layout.addWidget(btn)

        reset_btn = self.create_reset_button()
        button_layout.addWidget(reset_btn)

        widget = QWidget()
        widget.setLayout(button_layout)
        widget.setStyleSheet("background-color: silver;")

        dock_widget = QDockWidget("Shape Selection", self)
        dock_widget.setWidget(widget)
        dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)

        return dock_widget

    def create_shape_buttons(self):
        shapes = [("Triangle", "Triangle"), ("Rectangle", "Rectangle"), ("Square", "Square"),
                  ("Pentagon", "Pentagon"), ("Hexagon", "Hexagon"), ("Circle", "Circle")]

        return [self.create_shape_button(name, shape) for name, shape in shapes]

    def create_shape_button(self, name, shape):
        btn = QPushButton(name)
        btn.setStyleSheet("""
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
        btn.clicked.connect(lambda _, s=shape: self.set_shape_filter(s))
        return btn

    def create_reset_button(self):
        reset_btn = QPushButton("All shapes")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: yellow;
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
        reset_btn.clicked.connect(lambda: self.set_shape_filter(None))
        return reset_btn

    def show_info_popup(self):
        info_text = (
            "Click on a button to filter the shape detection to one shape only. "
            "Press 'All shapes' to detect all shapes again."
        )
        QMessageBox.information(self, "Shape Detection Info", info_text)


    def set_video_window_size(self, window_size):
        width, height = map(int, window_size)
        self.video_label.setFixedSize(width, height)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.video_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.create_buttons()

        window_width = int(self.camera_params['window_size'][0])
        window_height = int(self.camera_params['window_size'][1])
        self.setGeometry(100, 100, window_width, window_height)

    def set_shape_filter(self, shape):
        self.selected_shape = shape
        self.visualizer.set_shape_filter(shape)

    def update_frame(self):
        frame = self.camera.read_frame()
        if frame is not None:
            label_width = self.video_label.width()
            label_height = self.video_label.height()

            frame = cv2.resize(frame, (label_width, label_height))

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
