import os.path
import json

import yaml


class ConfigLoader(object):
    def __init__(self):
        self._map = {
            '.json': json.load,
            '.yaml': yaml.safe_load,
        }

    def load_config_file(self, filename):
        _, fileext = os.path.splitext(filename)
        load_fcn = self._map[fileext]
        with open(filename) as cfg_file:
            config = load_fcn(cfg_file)
        return config
