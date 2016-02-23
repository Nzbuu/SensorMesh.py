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

        # parse includes
        if isinstance(config, dict):
            config = self._parse_config(config)

        return config

    def _get_load_fcn(self, filename):
        _, fileext = os.path.splitext(filename)
        load_fcn = self._map[fileext]
        return load_fcn

    def _load_file(self, filename, load_fcn):
        with open(filename) as cfg_file:
            config = load_fcn(cfg_file)
        return config

    def _parse_config(self, config):
        include_file = config.pop('!include', None)
        include_node = config.pop('!include_node', None)

        for k in config:
            if isinstance(config[k], dict):
                config[k] = self._parse_config(config[k])

        if include_file:
            include_cfg = self.load_config_file(include_file)
            if include_node:
                include_cfg = include_cfg[include_node]

            config.update(include_cfg)

        return config
