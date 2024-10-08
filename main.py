import argparse
from src.modes import run_camera_mode, run_image_mode


def main():
    parser = argparse.ArgumentParser(description="Shape and Color Detection")
    parser.add_argument('--mode', type=str, choices=['CAMERA', 'IMAGE'], required=True,
                        help="Mode to run: 'CAMERA' for live feed, 'IMAGE' for static image analysis")

    args = parser.parse_args()

    if args.mode == 'CAMERA':
        run_camera_mode()
    elif args.mode == 'IMAGE':
        run_image_mode()


if __name__ == "__main__":
    main()
