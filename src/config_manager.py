import configparser

CONFIG_FILE = 'src/config.ini'


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config


def load_shape_params(config):
    return {
        'min_contour_area': int(config['SHAPE_DETECTION']['min_contour_area']),
        'canny_threshold1': int(config['SHAPE_DETECTION']['canny_threshold1']),
        'canny_threshold2': int(config['SHAPE_DETECTION']['canny_threshold2']),
        'blur_kernel_size': int(config['SHAPE_DETECTION']['blur_kernel_size'])
    }


def load_camera_params(config):
    return {
        'camera_index': int(config['CAMERA']['camera_index']),
        'window_size': config['CAMERA']['window_size'].split('x'),
        'fps': int(config['CAMERA']['fps']),

    }


def load_color_ranges(config, mode):
    if mode == 'CAMERA':
        color_config = 'COLOR_RANGES_CAMERA'
    else:
        color_config = 'COLOR_RANGES_IMAGE'

    return {
        'red': (tuple(map(int, config[color_config]['red_lower'].split(','))),
                tuple(map(int, config[color_config]['red_upper'].split(',')))),
        'green': (tuple(map(int, config[color_config]['green_lower'].split(','))),
                  tuple(map(int, config[color_config]['green_upper'].split(',')))),
        'blue': (tuple(map(int, config[color_config]['blue_lower'].split(','))),
                 tuple(map(int, config[color_config]['blue_upper'].split(',')))),
        'yellow': (tuple(map(int, config[color_config]['yellow_lower'].split(','))),
                   tuple(map(int, config[color_config]['yellow_upper'].split(',')))),
        'violet': (tuple(map(int, config[color_config]['violet_lower'].split(','))),
                   tuple(map(int, config[color_config]['violet_upper'].split(','))))
    }
