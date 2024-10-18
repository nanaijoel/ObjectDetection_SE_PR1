#ShapeAndColorDetection class, handles image processing
import cv2
import numpy as np


class ShapeAndColorDetection:
    def __init__(self, shape_params, color_ranges):
        self.shape_params = shape_params
        self.color_ranges = color_ranges

    @staticmethod
    def detect_shape(contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        vertices = len(approx)

        M = cv2.moments(contour)
        if M['m00'] == 0:
            return "undefined"

        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            extent = cv2.contourArea(contour) / (w * h)
            if 0.95 <= aspect_ratio <= 1.05 and 0.8 <= extent <= 1.0:
                return "Square"
            else:
                return "Rectangle"
        elif vertices == 5:
            return "Pentagon"
        elif vertices == 6:
            return "Hexagon"
        else:
            return "Circle"

    def detect_color(self, hsv, contour):
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)
        mean_hsv = cv2.mean(hsv, mask=mask)[:3]

        for color, (lower, upper) in self.color_ranges.items():
            lower = np.array(lower)
            upper = np.array(upper)
            if cv2.inRange(np.array([[mean_hsv]], dtype=np.uint8), lower, upper).any():
                return color
        return "undefined"

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (self.shape_params['blur_kernel_size'], self.shape_params['blur_kernel_size']),
                                   0)
        edges = cv2.Canny(blurred, self.shape_params['canny_threshold1'], self.shape_params['canny_threshold2'])

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        shapes = []
        for contour in contours:
            if cv2.contourArea(contour) > self.shape_params['min_contour_area']:
                shape = self.detect_shape(contour)
                color = self.detect_color(hsv, contour)
                shapes.append((contour, shape, color))
        return shapes
