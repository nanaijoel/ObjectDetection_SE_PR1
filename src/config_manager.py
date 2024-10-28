# Config class, handles reading the config file
import configparser

class ConfigManager:
    CONFIG_FILE = 'config.ini'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE)

    def load_shape_params(self, mode):
        """
        :param mode: CAMERA, IMAGE or GUI
        :return: config shape parameters
        """
        if mode == 'CAMERA':
            section = 'SHAPE_DETECTION_CAMERA'
        else:
            section = 'SHAPE_DETECTION_IMAGE'

        return {
            'min_contour_area': int(self.config[section]['min_contour_area']),
            'canny_threshold1': int(self.config[section]['canny_threshold1']),
            'canny_threshold2': int(self.config[section]['canny_threshold2']),
            'kernel_x': int(self.config[section]['kernel_x']),
            'kernel_y': int(self.config[section]['kernel_y']),
            'approx_poly_epsilon_factor': float(self.config[section]['approx_poly_epsilon_factor']),
            'tolerance': float(self.config[section]['tolerance'])
        }

    def load_camera_params(self):
        return {
            'camera_index': int(self.config['CAMERA']['camera_index']),
            'window_size': self.config['CAMERA']['window_size'].split('x'),
            'fps': int(self.config['CAMERA']['fps']),
        }

    def load_color_ranges(self, mode):
        """
        :param mode: IMAGE, CAMERA or GUI
        :return: config colour settings
        """
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
            'pink': (tuple(map(int, self.config[color_config]['pink_lower'].split(','))),
                     tuple(map(int, self.config[color_config]['pink_upper'].split(',')))),
            'violet': (tuple(map(int, self.config[color_config]['violet_lower'].split(','))),
                       tuple(map(int, self.config[color_config]['violet_upper'].split(',')))),
        }
