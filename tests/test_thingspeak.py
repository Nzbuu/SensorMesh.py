import pytest

from sensormesh.thingspeak import *


class TestThingspeakSource():
    def test_default_key_is_none(self):
        obj = ThingSpeakEndpoint()
        assert obj.get_key(write=False) is None

    def test_can_configure_key(self):
        obj = ThingSpeakEndpoint()
        obj.configure(read_key='ABCDEFGHIJKLMNOPQRST')
        assert obj.get_key(write=False) == 'ABCDEFGHIJKLMNOPQRST'


class TestThingspeakLogger():
    def test_no_key_is_error(self):
        obj = ThingSpeakEndpoint()
        with pytest.raises(ConfigurationError):
            obj.get_key(write=True)

    def test_can_configure_key(self):
        obj = ThingSpeakEndpoint()
        obj.configure(write_key='ZYXWVUTSRQP0987654321')
        assert obj.get_key(write=True) == 'ZYXWVUTSRQP0987654321'
