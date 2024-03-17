from configparser import ConfigParser
import os.path

def get_config():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_filepath = dir_path + "/config.ini"

    # Check if the config file exists
    exists = os.path.exists(config_filepath)
    config = None

    if exists:
        print("--------config.ini file found at", config_filepath)
        config = ConfigParser()
        config.read(config_filepath)
        return config
    else:
        print("---------config.ini file not found at", config_filepath)

def get_database_config(key):
    config = get_config()
    if config is None:
        return None
    db_config = config["DATABASE"]
    return db_config[key]

def get_html_config(key):
    config = get_config()
    if config is None:
        return None
    html_config = config["HTML"]
    return html_config[key]