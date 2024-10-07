import cv2
import os
from src.ShapeAndColorDetection import process_frame  # Import the existing shape and color detection logic
from src.logger import DataLogger
from src.visualize_shapes import visualize_shapes


# Function to run the camera mode
def run_camera_mode(config):
    camera_index = int(config['CAMERA']['camera_index'])
    window_size = config['CAMERA']['window_size'].split('x')
    fps = int(config['CAMERA']['fps'])
    log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')

    # Initialize the logger
    logger = DataLogger(log_file)

    # Set up the camera
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(window_size[0]))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(window_size[1]))
    cap.set(cv2.CAP_PROP_FPS, fps)

    # Start reading frames from the camera
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame to detect shapes and colors
        shapes = process_frame(frame, logger, config)

        # Visualize the detected shapes and colors on the frame
        frame_with_shapes = visualize_shapes(frame, shapes)

        # Show the frame in a window
        cv2.imshow("Camera Feed", frame_with_shapes)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()


# Function to run the image mode
def run_image_mode(config):
    image_directory = config['IMAGE']['image_directory']
    log_file = os.path.join(config['DEFAULT']['log_folder'], 'data_log.csv')

    # Initialize the logger
    logger = DataLogger(log_file)

    # Loop through all image files in the directory
    for filename in os.listdir(image_directory):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_directory, filename)
            image = cv2.imread(image_path)

            if image is None:
                print(f"Error loading image: {filename}")
                continue

            # Process the image to detect shapes and colors
            shapes = process_frame(image, logger, config)

            # Visualize the detected shapes and colors on the image
            image_with_shapes = visualize_shapes(image, shapes)
            cv2.imshow(f"Image: {filename}", image_with_shapes)
            cv2.waitKey(0)

    # Close all windows after processing all images
    cv2.destroyAllWindows()
