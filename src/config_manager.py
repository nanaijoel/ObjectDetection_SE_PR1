# Config class, handles reading the config file

import configparser


class ConfigManager:
    CONFIG_FILE = 'config.ini'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE)

    def load_shape_params(self):
        return {
            'min_contour_area': int(self.config['SHAPE_DETECTION']['min_contour_area']),
            'canny_threshold1': int(self.config['SHAPE_DETECTION']['canny_threshold1']),
            'canny_threshold2': int(self.config['SHAPE_DETECTION']['canny_threshold2']),
            'blur_kernel_size': int(self.config['SHAPE_DETECTION']['blur_kernel_size']),
            'approx_poly_epsilon_factor': float(self.config['SHAPE_DETECTION']['approx_poly_epsilon_factor']),
            'aspect_ratio_tolerance': float(self.config['SHAPE_DETECTION']['aspect_ratio_tolerance']),
            'extent_threshold': float(self.config['SHAPE_DETECTION']['extent_threshold'])
        }

    def load_camera_params(self):
        return {
            'camera_index': int(self.config['CAMERA']['camera_index']),
            'window_size': self.config['CAMERA']['window_size'].split('x'),
            'fps': int(self.config['CAMERA']['fps']),
        }

    def load_color_ranges(self, mode):
        if mode == 'CAMERA':
            color_config = 'COLOR_RANGES_CAMERA'
        else:
            color_config = 'COLOR_RANGES_IMAGE'

        return {
            'red': (tuple(map(int, self.config[color_config]['red_lower'].split(','))),
                    tuple(map(int, self.config[color_config]['red_upper'].split(',')))),
            'green': (tuple(map(int, self.config[color_config]['green_lower'].split(','))),
                      tuple(map(int, self.config[color_config]['green_upper'].split(',')))),
            'blue': (tuple(map(int, self.config[color_config]['blue_lower'].split(','))),
                     tuple(map(int, self.config[color_config]['blue_upper'].split(',')))),
            'yellow': (tuple(map(int, self.config[color_config]['yellow_lower'].split(','))),
                       tuple(map(int, self.config[color_config]['yellow_upper'].split(',')))),
            'violet': (tuple(map(int, self.config[color_config]['violet_lower'].split(','))),
                       tuple(map(int, self.config[color_config]['violet_upper'].split(','))))
        }
