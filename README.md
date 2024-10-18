# ObjectDetection_SE_PR1

Webcam application which identifies geometrical objects such as triangles, rectangles, circles, pentagons and hexagons in different colors in the camera's field of view.

Further, there is a mode to also analyze the shapes in images put in the image folder.

# Features

    - Detects shapes like triangles, circles, and rectangles.
    - Recognizes objects in different colors (e.g., red, green, blue).
    - Supports image-based and live webcam detection modes.


# How to Use

    1. Install dependencies:
    - Use the provided requirements.txt file to set up the recommended virtual environment 
      with the correct module versions.
    - Install the dependencies by running: pip install -r requirements.txt
    - Otherwise, just check the version of the specific modules which we use


    2. Run the application:
    - Navigate to the project folder and run: python main.py --mode <mode_name>
      Available modes: 
      IMAGE: Detects shapes and colors in images from the input directory. 
      CAMERA: Detects shapes and colors using the webcam.
      For example, type python main.py --mode CAMERA to run the application in camera mode.
    - To close the camera or image windows and quit the program, press the 'q' key. 

# Configuration

    - Modify detection settings (e.g., contour thresholds, color ranges) in the config.ini file. 
    - Log files and image input paths are also configurable.
    - To find the active camera IDs on your system, you can run the camera.py file. 
      This will return the IDs of all active cameras that are available for use.
      By default, the camera ID is set to 0, but you can change the ID in the config.ini file.

# Ongoing developments

    - GUI mode: The mode is defined in the config.ini file but is not implemented yet.


# Optimizations

    - The detection algorithm could be further optimized for better accuracy and performance.
    - The color recognition could be expanded to include more color ranges.
    - The data_log.csv could log only shapes that are recognized over a period of time to filter random detections
