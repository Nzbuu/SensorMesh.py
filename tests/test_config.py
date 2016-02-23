import unittest.mock as mock
import json

import yaml

from sensormesh.config import ConfigManager


class TestConfigManager:
    def test_can_read_empty_json_file(self):
        test_data = {}
        cfg_man = ConfigManager()

        mock_file = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('builtins.open', mock_file):
            cfg_data = cfg_man.load_config_file('config.json')

        assert cfg_data == test_data

    def test_can_read_json_config_file(self):
        test_data = {'name': 'test_thing', 'key': 'ABCDEFGHIJ', 'feed': {'field1': 'A'}}
        read_data = json.dumps(test_data)

        cfg_man = ConfigManager()

        mock_file = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_file):
            cfg_data = cfg_man.load_config_file('config.json')

        assert cfg_data == test_data

    def test_can_read_yaml_config_file(self):
        test_data = {'name': 'test_thing', 'key': 'ABCDEFGHIJ', 'feed': {'field1': 'A'}}
        read_data = yaml.dump(test_data)

        cfg_man = ConfigManager()

        mock_file = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_file):
            cfg_data = cfg_man.load_config_file('config.yaml')

        assert cfg_data == test_data

    def test_selects_correct_loader(self):
        mock_test = mock.Mock(return_value={})
        mock_cnfg = mock.Mock(return_value={})

        cfg_man = ConfigManager()
        cfg_man._map = {'.test': mock_test, '.cnfg': mock_cnfg}
        cfg_data = cfg_man.load_config_file('/folder/config.cnfg')

        assert cfg_data == {}
        mock_cnfg.assert_called_once_with('/folder/config.cnfg')
        assert not mock_test.called
