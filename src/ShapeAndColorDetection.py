<<<<<<< HEAD
""" 
Real-Time Shape and Color Detection Module

Description:
Detecting geometric shapes and colors in real-time using
live camera feed or static images. 
Identification of shapes like triangles, rectangles, squares, and circles, 
and their colors (red, green, blue, yellow, and violet. 
Detection data is logged into a CSV file with timestamps. 
Command-line arguments enable switching between 
camera and image modes and setting log output directories.

(Riaan Kaempfer, 07.10.2024)
"""

import cv2
import numpy as np
import argparse
import os
import csv
from datetime import datetime

# Define the color ranges for detection
color_ranges = {
    'red': [(0, 100, 100), (10, 255, 255)],
    'green': [(40, 40, 40), (70, 255, 255)],
    'blue': [(90, 50, 50), (130, 255, 255)],
    'yellow': [(20, 100, 100), (30, 255, 255)],
    'violet': [(140, 100, 100), (160, 255, 255)]
}

# Function to detect the color within a contour
def detect_color(hsv, contour):
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)  # Create a mask for the contour
    cv2.drawContours(mask, [contour], -1, 255, -1)  # Draw the contour on the mask
    mean_hsv = cv2.mean(hsv, mask=mask)[:3]  # Get the mean HSV value inside the contour
    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower)  # Convert lower bound to numpy array
        upper = np.array(upper)  # Convert upper bound to numpy array
        # Check if mean_hsv lies within the color range
        if cv2.inRange(np.array([[mean_hsv]], dtype=np.uint8), lower, upper).any():
            return color
    return "undefined"

# Function to detect the shape of a contour
def detect_shape(contour):
    peri = cv2.arcLength(contour, True)  # Perimeter of the contour
    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)  # Approximate the contour's shape
    vertices = len(approx)  # Number of vertices in the shape

    if vertices == 3:
        return "Triangle"
    elif vertices == 4:
        # Check if the shape is a square or rectangle
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

# Process frames from the camera or images in the folder
def process_frame(frame, writer):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert the frame to HSV color space
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian blur
    edges = cv2.Canny(blurred, 50, 150)  # Detect edges in the frame
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours

    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Ignore small contours
            shape = detect_shape(contour)  # Detect the shape
            color = detect_color(hsv, contour)  # Detect the color
            M = cv2.moments(contour)  # Calculate moments to find the center of the shape
            if M["m00"] > 0:
                cX = int(M["m10"] / M["m00"])  # X-coordinate of the shape's center
                cY = int(M["m01"] / M["m00"])  # Y-coordinate of the shape's center
                cv2.putText(frame, f"{shape}, {color}", (cX - 50, cY),  # Label the shape and color on the frame
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                # Log the information into the CSV file
                writer.writerow([datetime.now(), shape, color])

    return frame

# Main function to handle command-line arguments and processing
def main():
    parser = argparse.ArgumentParser(description="Shape and Color Detection")
    # Set 'required=False', if passing cmd-line-arguments should be accepted!:
    parser.add_argument('--mode', required=False, choices=['CAMERA', 'IMAGE'], help='Operation mode: CAMERA or IMAGE')
    parser.add_argument('--folder', help='Folder containing images (for IMAGE mode)')
    parser.add_argument('--log_folder', required=False, help='Folder to save CSV log files')
    args = parser.parse_args()
    
    # Set default values if arguments are not provided
    if args.mode is None:
        args.mode = "CAMERA"  # Default to CAMERA mode
    if args.log_folder is None:
        args.log_folder = "./logs"  # Default log folder

    # Create the log folder if it doesn't exist
    if not os.path.exists(args.log_folder):
        os.makedirs(args.log_folder)

    # Prepare the CSV file for logging
    log_file = os.path.join(args.log_folder, "detections.csv")
    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Shape', 'Color'])

        if args.mode == 'CAMERA':
            # Open the camera feed
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Unable to open camera.")
                return

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                # Process each frame
                frame = process_frame(frame, writer)
                cv2.imshow("Camera Feed", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                    break

            cap.release()
            cv2.destroyAllWindows()

        elif args.mode == 'IMAGE':
            if not args.folder:
                print("Error: Folder path is required in IMAGE mode.")
                return

            # Process each image in the folder
            for filename in os.listdir(args.folder):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(args.folder, filename)
                    frame = cv2.imread(img_path)
                    if frame is not None:
                        frame = process_frame(frame, writer)
                        cv2.imshow(f"Image - {filename}", frame)
                        cv2.waitKey(0)  # Press any key to move to the next image

            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
=======
<<<<<<< HEAD
""" 
Real-Time Shape and Color Detection Module

Description:
Detecting geometric shapes and colors in real-time using
live camera feed or static images. 
Identification of shapes like triangles, rectangles, squares, and circles, 
and their colors (red, green, blue, yellow, and violet. 
Detection data is logged into a CSV file with timestamps. 
Command-line arguments enable switching between 
camera and image modes and setting log output directories.
"""

import cv2
import numpy as np


class ShapeAndColorDetection:
    def __init__(self, shape_params, color_ranges):
        self.shape_params = shape_params
        self.color_ranges = color_ranges

    def detect_shape(self, contour):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, self.shape_params['approx_poly_epsilon_factor'] * peri, True)
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
            if ((1 - self.shape_params['aspect_ratio_tolerance'])
                    <= aspect_ratio <= (1 + self.shape_params['aspect_ratio_tolerance'])
                    and extent >= self.shape_params['extent_threshold']):
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
        blurred = cv2.GaussianBlur(gray, (self.shape_params['blur_kernel_size'],
                                          self.shape_params['blur_kernel_size']), 0)
        edges = cv2.Canny(blurred, self.shape_params['canny_threshold1'], self.shape_params['canny_threshold2'])

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        shapes = []
        for contour in contours:
            if cv2.contourArea(contour) > self.shape_params['min_contour_area']:
                shape = self.detect_shape(contour)
                color = self.detect_color(hsv, contour)
                shapes.append((contour, shape, color))
        return shapes
=======
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
>>>>>>> 7c0276ffdeb4ce20df7e958422c687bfa01d357a
>>>>>>> develop
