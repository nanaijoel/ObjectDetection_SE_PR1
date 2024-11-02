# ObjectDetection_SE_PR1

Webcam application which identifies geometrical objects such as triangles, rectangles, circles, pentagons and hexagons in different colors in the camera's field of view.

Further, there is a mode to also analyze the shapes in images put in the image folder.

The repository relies solely on the Python programming language.

# Features

- Detects shapes like triangles, circles, and rectangles, pentagons and hexagons.
- Recognizes objects in different colors (red, green, blue, yellow, violet).
- Supports image-based and live webcam detection modes.
- In GUI mode, you can filter by a single shape type or view all shape types together.


# How to Use

1. Get repository:
- Clone the repository to your local development environment (e.g., your IDE) using the following command:

  ```
  git clone https://github.com/nanaijoel/ObjectDetection_SE_PR1.git
  ```

- Alternatively you can download the project as a zip file from github and copy or move the project into your IDE.


2. Install dependencies:
- Make sure you use a python version 3.xx, so libraries like csv, datetime, configparser, os and sys are included directly.
- Use the provided requirements.txt file to set up the recommended virtual environment with the correct module versions.
- Install the dependencies by running:

  ```
  pip install -r requirements.txt
  ```

- Otherwise, just check the version of the specific modules which we use and get them on your IDE.


3. Run the application:
- Navigate to the project folder and run: python main.py --mode <mode_name>
  Available modes: 
  IMAGE: Detects shapes and colors in images from the input directory. 
  CAMERA: Detects shapes and colors using the webcam.
  GUI: Different buttons for shapes. That way the logger and visualization will only react to the selected shape.

For example, to run the application in camera mode, type in terminal:

  ```
  python main.py --mode CAMERA
  ```

- To close the camera or image windows and quit the program, press the 'q' key. 

# Configuration

- Modify detection settings (e.g., contour thresholds, color ranges) in the config.ini file. 
- Log files and image input paths are also configurable.
- To find the active camera IDs on your system, you can run the camera.py file. 
  This will return the IDs of all active cameras that are available for use.
  By default, the camera ID is set to 0, but you can change the ID in the config.ini file.

# Ongoing developments

- GUI mode: Adding 3 sliders for Hue, Saturation and Value, so we can modify the camera frame in real time. 


# Optimizations

- The detection algorithm could be further optimized for better accuracy and performance.
- The color recognition could be expanded to include more color ranges.
- Color recognition could be implemented dynamically. At the moment, you have to adjust the values of the parameters
  according to the current lighting conditions.
