import os.path
import json

import yaml


class ConfigLoader(object):
    def __init__(self):
        self._map = {
            '.json': self.load_json_file,
            '.yaml': self.load_yaml_file,
        }

    def load_config_file(self, filename):
        _, fileext = os.path.splitext(filename)
        load_fcn = self._map[fileext]
        config = load_fcn(filename)
        return config

    def load_json_file(self, filename):
        with open(filename) as cfg_file:
            cfg_data = json.load(cfg_file)
        return cfg_data

    def load_yaml_file(self, filename):
        with open(filename) as cfg_file:
            cfg_data = yaml.safe_load(cfg_file)
        return cfg_data
