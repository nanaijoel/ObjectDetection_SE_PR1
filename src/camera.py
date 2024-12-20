# Camera class, handles initialization and readout of the camera.

import cv2


class Camera:
    def __init__(self, camera_params):
        self.camera_params = camera_params
        self.cap = None

    def initialize_camera(self):
        """
        Initializes the camera with the specified index, FPS, and window size.
        FPS and window size are checked automatically.
        :return: cv2.VideoCapture object for the camera.
        """
        self.cap = cv2.VideoCapture(self.camera_params['camera_index'])
        self.cap.set(cv2.CAP_PROP_FPS, self.camera_params['fps'])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.camera_params['window_size'][0]))
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.camera_params['window_size'][1]))
        return self.cap

    def read_frame(self):
        """
        Reads the next frame from the camera.
        :return: new frame if available, else None.
        """
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def release_camera(self):

        if self.cap is not None:
            self.cap.release()

    def get_info(self):
        """
        Get information about the camera such as window size, FPS, and camera index.
        :return: Dictionary with camera info or message if camera is not initialized.
        """
        if self.cap is not None and self.cap.isOpened():
            return {
                'Resolution': (self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'FPS': self.cap.get(cv2.CAP_PROP_FPS),
                'Camera Index': self.camera_params['camera_index']
            }
        return "Camera is not initialized or not opened."

    @staticmethod
    def close_window():
        cv2.destroyAllWindows()

    @staticmethod
    def list_webcams():
        """
        Lists available webcams connected to the system.
        :return: List of available camera indices.
        """
        index = 0
        arr = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append(index)
            cap.release()
            index += 1
        return arr


if __name__ == "__main__":
    available_cameras = Camera.list_webcams()
    print("Available camera IDs:", available_cameras)