import cv2
import numpy as np


# Function to detect shape based on contour
def detect_shape(contour):
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
    vertices = len(approx)

    if vertices == 3:
        return "Triangle"
    elif vertices == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if 0.95 <= aspect_ratio <= 1.05:
            return "Square"
        else:
            return "Rectangle"
    elif vertices == 5:
        return "Pentagon"
    elif vertices == 6:
        return "Hexagon"
    else:
        return "Circle"


# Function to detect color inside a given contour
def detect_color(hsv, contour, color_ranges):
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, 255, -1)
    mean_hsv = cv2.mean(hsv, mask=mask)[:3]

    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower)
        upper = np.array(upper)
        if cv2.inRange(np.array([[mean_hsv]], dtype=np.uint8), lower, upper).any():
            return color
    return "undefined"


# Function to process frames and detect shapes and colors
def process_frame(frame, shape_params, color_ranges):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (shape_params['blur_kernel_size'], shape_params['blur_kernel_size']), 0)
    edges = cv2.Canny(blurred, shape_params['canny_threshold1'], shape_params['canny_threshold2'])

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []
    for contour in contours:
        if cv2.contourArea(contour) > shape_params['min_contour_area']:
            shape = detect_shape(contour)
            color = detect_color(hsv, contour, color_ranges)
            shapes.append((contour, shape, color))

    return shapes
