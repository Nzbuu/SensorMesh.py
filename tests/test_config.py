from unittest.mock import patch, mock_open, Mock
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

    def test_selects_correct_loader(self):
        cfg_man = ConfigManager()
        mock_load = Mock(return_value={})
        cfg_man._map['.test'] = mock_load
        cfg_data = cfg_man.load_config_file('/folder/config.test')

        assert cfg_data == {}
        mock_load.assert_called_once_with('/folder/config.test')
