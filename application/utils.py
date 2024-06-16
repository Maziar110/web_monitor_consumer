import yaml
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


def load_config_file(config_file_path) -> dict|None:
    '''
    looks for config.yaml and if exists, 
    returns the variabls.
    '''
    if not os.path.exists(config_file_path):
        logging.error("Unable to find config file")
        return None
    with open(config_file_path, "r") as file:
        return yaml.safe_load(file)


