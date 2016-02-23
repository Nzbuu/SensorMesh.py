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
        # select loader
        load_fcn = self._get_load_fcn(filename)

        # load file
        config = self._load_file(filename, load_fcn)

        return config

    def _get_load_fcn(self, filename):
        _, fileext = os.path.splitext(filename)
        load_fcn = self._map[fileext]
        return load_fcn

    def _load_file(self, filename, load_fcn):
        with open(filename) as cfg_file:
            config = load_fcn(cfg_file)
        return config
