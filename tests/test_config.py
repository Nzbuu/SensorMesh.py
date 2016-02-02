from unittest.mock import patch, mock_open
import json
import builtins

from sensormesh.applications import load_config_file


def test_can_read_config_file():
    test_data = {'name': 'test_thing', 'key': 'ABCDEFGHIJ', 'feed': {'field1': 'A'}}
    with patch.object(builtins, 'open', mock_open(read_data=json.dumps(test_data))):
        cfg_data = load_config_file('config.json')

    assert cfg_data == test_data
