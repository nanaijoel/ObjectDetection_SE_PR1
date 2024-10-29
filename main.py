# main file, runs the program
import argparse
from src.modes import AppRunner


def main():
    parser = argparse.ArgumentParser(description="Shape and Color Detection")
    parser.add_argument('--mode', type=str, choices=['CAMERA', 'IMAGE', 'GUI'], required=True,
                        help="'CAMERA' for live feed, 'IMAGE' for static analysis, 'GUI' for interactive GUI")
    args = parser.parse_args()

    app_runner = AppRunner(args.mode)

    if args.mode == 'CAMERA':
        app_runner.run_camera_mode()
    elif args.mode == 'IMAGE':
        app_runner.run_image_mode()
    elif args.mode == 'GUI':
        app_runner.run_gui_mode()


if __name__ == "__main__":
    main()
