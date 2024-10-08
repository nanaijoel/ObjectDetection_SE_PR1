import argparse
from src.config_manager import load_config
from src.modes import run_camera_mode, run_image_mode


def main():

    config = load_config()

    # Set up argument parser for mode selection
    parser = argparse.ArgumentParser(description="Shape and Color Detection")
    parser.add_argument('--mode', required=True, choices=['CAMERA', 'IMAGE'],
                        help="Choose the mode of operation: CAMERA or IMAGE")
    args = parser.parse_args()

    if args.mode == 'CAMERA':
        run_camera_mode(config)
    elif args.mode == 'IMAGE':
        run_image_mode(config)


if __name__ == "__main__":
    main()
