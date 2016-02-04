from unittest.mock import patch, mock_open
import json
import builtins

from sensormesh.application import ConfigManager


class TestConfigManager:
    def test_can_read_empty_json_file(self):
        test_data = {}
        cfg_man = ConfigManager()
        with patch.object(builtins, 'open', mock_open(read_data=json.dumps(test_data))):
            cfg_data = cfg_man.load_config_file('config.json')

        assert cfg_data == test_data

    def test_can_read_json_config_file(self):
        test_data = {'name': 'test_thing', 'key': 'ABCDEFGHIJ', 'feed': {'field1': 'A'}}
        cfg_man = ConfigManager()
        with patch.object(builtins, 'open', mock_open(read_data=json.dumps(test_data))):
            cfg_data = cfg_man.load_config_file('config.json')

        assert cfg_data == test_data
