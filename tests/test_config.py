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
        mock_test = Mock(return_value={})
        mock_cnfg = Mock(return_value={})

        cfg_man = ConfigManager()
        cfg_man._map = {'.test': mock_test, '.cnfg': mock_cnfg}
        cfg_data = cfg_man.load_config_file('/folder/config.cnfg')

        assert cfg_data == {}
        mock_cnfg.assert_called_once_with('/folder/config.cnfg')
        assert not mock_test.called
