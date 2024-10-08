import cv2
import numpy as np

def load_color_ranges(config):
    return {
        'red': (tuple(map(int, config['COLOR_RANGES']['red_lower'].split(','))),
                tuple(map(int, config['COLOR_RANGES']['red_upper'].split(',')))),
        'green': (tuple(map(int, config['COLOR_RANGES']['green_lower'].split(','))),
                  tuple(map(int, config['COLOR_RANGES']['green_upper'].split(',')))),
        'blue': (tuple(map(int, config['COLOR_RANGES']['blue_lower'].split(','))),
                 tuple(map(int, config['COLOR_RANGES']['blue_upper'].split(',')))),
        'yellow': (tuple(map(int, config['COLOR_RANGES']['yellow_lower'].split(','))),
                   tuple(map(int, config['COLOR_RANGES']['yellow_upper'].split(',')))),
        'violet': (tuple(map(int, config['COLOR_RANGES']['violet_lower'].split(','))),
                   tuple(map(int, config['COLOR_RANGES']['violet_upper'].split(','))))
    }

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

# Function to detect shape based on the contour
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
    else:
        return "Circle"

# Function to process frames and detect shapes and colors
def process_frame(frame, logger, config):
    color_ranges = load_color_ranges(config)

    min_contour_area = int(config['SHAPE_DETECTION']['min_contour_area'])
    canny_threshold1 = int(config['SHAPE_DETECTION']['canny_threshold1'])
    canny_threshold2 = int(config['SHAPE_DETECTION']['canny_threshold2'])
    blur_kernel_size = int(config['SHAPE_DETECTION']['blur_kernel_size'])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (blur_kernel_size, blur_kernel_size), 0)

    edges = cv2.Canny(blurred, canny_threshold1, canny_threshold2)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            shape = detect_shape(contour)
            color = detect_color(hsv, contour, color_ranges)
            M = cv2.moments(contour)
            if M["m00"] > 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                shapes.append((contour, shape, color))
                logger.log_data(shape, color)

    return shapes
