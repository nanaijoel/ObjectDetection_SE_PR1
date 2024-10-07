import configparser

CONFIG_FILE = 'config.ini'

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def save_config(new_config):
    with open(CONFIG_FILE, 'w') as configfile:
        new_config.write(configfile)
