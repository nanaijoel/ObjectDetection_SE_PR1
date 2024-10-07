import argparse
from config_manager import load_config
from modes import run_camera_mode, run_image_mode

def main():
    # Load the configuration file
    config = load_config()

    # Set up argument parser for mode selection
    parser = argparse.ArgumentParser(description="Shape and Color Detection")
    parser.add_argument('--mode', required=True, choices=['CAMERA', 'IMAGE'],
                        help="Choose the mode of operation: CAMERA or IMAGE")
    args = parser.parse_args()

    # Call the appropriate function based on the selected mode
    if args.mode == 'CAMERA':
        run_camera_mode(config)
    elif args.mode == 'IMAGE':
        run_image_mode(config)

if __name__ == "__main__":
    main()
