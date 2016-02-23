import unittest.mock as mock
import json

import yaml

from sensormesh.config import ConfigLoader


class TestConfigManager:
    def test_can_read_empty_json_file(self):
        test_data = {}
        cnfgr = ConfigLoader()

        mock_file = mock.mock_open(read_data=json.dumps(test_data))
        with mock.patch('builtins.open', mock_file):
            cfg_data = cnfgr.load_config_file('config.json')

        assert cfg_data == test_data

    def test_can_read_json_config_file(self):
        test_data = {'name': 'test_thing', 'key': 'ABCDEFGHIJ', 'feed': {'field1': 'A'}}
        read_data = json.dumps(test_data)

        cnfgr = ConfigLoader()

        mock_file = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_file):
            cfg_data = cnfgr.load_config_file('config.json')

        assert cfg_data == test_data

    def test_can_read_yaml_config_file(self):
        test_data = {'name': 'test_thing', 'key': 'ABCDEFGHIJ', 'feed': {'field1': 'A'}}
        read_data = yaml.dump(test_data)

        cnfgr = ConfigLoader()

        mock_file = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_file):
            cfg_data = cnfgr.load_config_file('config.yaml')

        assert cfg_data == test_data

    def test_selects_correct_loader(self):
        mock_test = mock.Mock()
        mock_cnfg = mock.Mock()

        cnfgr = ConfigLoader()
        cnfgr._map = {'.test': mock_test, '.cnfg': mock_cnfg}
        cnfgr._load_file = mock.Mock(return_value={})

        cfg_data = cnfgr.load_config_file('/folder/config.cnfg')

        assert cfg_data == {}
        cnfgr._load_file.assert_called_once_with('/folder/config.cnfg', mock_cnfg)
