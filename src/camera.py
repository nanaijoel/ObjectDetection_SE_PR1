import cv2



class Camera:
    def __init__(self, camera_params):
        self.camera_params = camera_params
        self.cap = None

    def initialize_camera(self):
        self.cap = cv2.VideoCapture(self.camera_params['camera_index'])
        self.cap.set(cv2.CAP_PROP_FPS, self.camera_params['fps'])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.camera_params['window_size'][0]))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.camera_params['window_size'][1]))
        return self.cap

    def read_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release_camera(self):
        if self.cap is not None:
            self.cap.release()

    def get_info(self):
        if self.cap is not None and self.cap.isOpened():
            return {
                'Resolution': (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'FPS': self.cap.get(cv2.CAP_PROP_FPS),
                'Camera Index': self.camera_params['camera_index']
            }
        return "Camera is not initialized or not opened."

    def close_window(self):
        cv2.destroyAllWindows()
