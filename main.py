#main file, runs the program
import argparse
from src.modes import AppRunner


def main():
    parser = argparse.ArgumentParser(description="Shape and Color Detection")
    parser.add_argument('--mode', type=str, choices=['CAMERA', 'IMAGE'], required=True,
                        help="Mode to run: 'CAMERA' for live feed, 'IMAGE' for static image analysis")
    args = parser.parse_args()

    app_runner = AppRunner(args.mode)

    if args.mode == 'CAMERA':
        app_runner.run_camera_mode()
    elif args.mode == 'IMAGE':
        app_runner.run_image_mode()


if __name__ == "__main__":
    main()
