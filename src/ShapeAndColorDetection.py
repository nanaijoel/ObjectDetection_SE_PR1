# ShapeAndColorDetection class, handles image processing

import cv2
import numpy as np


class ShapeAndColorDetection:
    def __init__(self, shape_params, color_ranges):
        self.shape_params = shape_params
        self.color_ranges = color_ranges

    def detect_shape(self, contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, self.shape_params['approx_poly_epsilon_factor'] * peri, True)
        return self.get_shape(approx, contour, peri)

    def get_shape(self, approx, contour, peri):
        """
        :return: the Form
        """
        vertices = len(approx)

        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            return self._detect_quadrilateral(approx)
        elif vertices == 5:
            return "Pentagon"
        elif vertices == 6:
            return "Hexagon"
        else:
            return self._detect_circle(contour, peri)

    def _detect_quadrilateral(self, approx):
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if (1 - self.shape_params['tolerance']) <= aspect_ratio <= (1 + self.shape_params['tolerance']):
            return "Square"
        return "Rectangle"

    @staticmethod
    def _detect_circle(contour, peri):
        area = cv2.contourArea(contour)
        circularity = 4 * np.pi * (area / (peri * peri))
        if circularity > 0.4:
            return "Circle"
        return "undefined"

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

    def process_frame(self, frame, target_shape=None):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (self.shape_params['kernel_x'], self.shape_params['kernel_y']), 0)
        edges = cv2.Canny(blurred, self.shape_params['canny_threshold1'], self.shape_params['canny_threshold2'])

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        shapes = []
        for contour in contours:
            if cv2.contourArea(contour) > self.shape_params['min_contour_area']:
                shape = self.detect_shape(contour)
                if target_shape is None or shape == target_shape:
                    color = self.detect_color(hsv, contour)
                    shapes.append((contour, shape, color))
        return shapes
