# ObjectDetection_SE_PR1
Webcam application which identifies geometrical objects such as triangles, circles, rectangles in different colors
in the camera's field of view.


# Features
- Detects shapes like triangles, circles, and rectangles.
- Recognizes objects in different colors (e.g., red, green, blue).
- Supports image-based and live webcam detection modes.


# How to Use
1. Install dependencies:
- Use the provided requirements.txt file to set up the recommended virtual environment with the correct module versions.
- Install the dependencies by running: pip install -r requirements.txt
- Otherwise, just check the version of the specific modules which we use

2. Run the application:
- Navigate to the project folder and run:  python main.py --mode <mode_name>
  - Available modes:
    IMAGE: Detects shapes and colors in images from the input directory.
    CAMERA: Detects shapes and colors using the webcam.
    GUI: (Under development)


# Configuration
Modify detection settings (e.g., contour thresholds, color ranges) in the config.ini file.
Log files and image input paths are also configurable.


# Ongoing developments
GUI mode: The mode is defined in the config.ini file but is not fully implemented yet.


# Optimizations
- The detection algorithm could be further optimized for better accuracy and performance.
- The color recognition could be expanded to include more color ranges.