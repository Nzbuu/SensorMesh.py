import pytest
import responses
import json

from sensormesh.thingspeak import *


class TestThingSpeakSource():
    def test_default_key_is_none(self):
        obj = ThingSpeakEndpoint()
        assert obj.get_key(write=False) is None

    def test_can_configure_key(self):
        obj = ThingSpeakEndpoint()
        obj.configure(read_key='ABCDEFGHIJKLMNOPQRST')
        assert obj.get_key(write=False) == 'ABCDEFGHIJKLMNOPQRST'

    @responses.activate
    def test_can_get_config_from_url(self):
        obj = ThingSpeakEndpoint()
        obj.configure(id=3, read_key='ABCDEFGHIJKLMNOPQRST')

        with responses.RequestsMock() as responses_:
            responses_.add(
                    responses.GET,
                    'https://api.thingspeak.com/channels/3/feed.json',
                    json=canned_responses['https://api.thingspeak.com/channels/3/feed.json']
            )
            info = obj.read_info()

            assert len(responses_.calls) == 1
            the_request = responses_.calls[0].request
            assert the_request.url == 'https://api.thingspeak.com/channels/3/feed.json?results=0'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ABCDEFGHIJKLMNOPQRST'

        assert info['name'] == 'ioBridge Server'
        assert info['field1'] == 'Server Temp'

    @responses.activate
    def test_can_configure_from_url(self):
        obj = ThingSpeakEndpoint()
        obj.configure(id=3, read_key='ABCDEFGHIJKLMNOPQRST')

        with responses.RequestsMock() as responses_:
            responses_.add(
                    responses.GET,
                    'https://api.thingspeak.com/channels/3/feed.json',
                    json=canned_responses['https://api.thingspeak.com/channels/3/feed.json']
            )
            obj.read_config()

            assert len(responses_.calls) == 1
            the_request = responses_.calls[0].request
            assert the_request.url == 'https://api.thingspeak.com/channels/3/feed.json?results=0'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ABCDEFGHIJKLMNOPQRST'

        assert obj.name == 'ioBridge Server'

    @responses.activate
    def test_can_read_data_from_url(self):
        obj = ThingSpeakEndpoint()
        obj.configure(id=3, field1='Server Temp')

        with responses.RequestsMock() as responses_:
            responses_.add(
                    responses.GET,
                    'https://api.thingspeak.com/channels/3/feed/last.json',
                    json=canned_responses['https://api.thingspeak.com/channels/3/feed/last.json']
            )
            data = obj.read()

        assert data['timestamp'] == 1453927930
        assert data['Server Temp'] == '58.5 F'


class TestThingSpeakLogger():
    def test_no_key_is_error(self):
        obj = ThingSpeakEndpoint()
        with pytest.raises(ConfigurationError):
            obj.get_key(write=True)

    def test_can_configure_key(self):
        obj = ThingSpeakEndpoint()
        obj.configure(write_key='ZYXWVUTSRQP0987654321')
        assert obj.get_key(write=True) == 'ZYXWVUTSRQP0987654321'

    @responses.activate
    def test_can_get_config_from_url(self):
        obj = ThingSpeakEndpoint()
        obj.configure(id=3, write_key='ZYXWVUTSRQP0987654321')

        with responses.RequestsMock() as responses_:
            responses_.add(
                    responses.GET,
                    'https://api.thingspeak.com/channels/3/feed.json',
                    json=canned_responses['https://api.thingspeak.com/channels/3/feed.json']
            )
            info = obj.read_info()

            assert len(responses_.calls) == 1
            the_request = responses_.calls[0].request
            assert the_request.url == 'https://api.thingspeak.com/channels/3/feed.json?results=0'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ZYXWVUTSRQP0987654321'

        assert info['name'] == 'ioBridge Server'
        assert info['field1'] == 'Server Temp'

    @responses.activate
    def test_can_configure_from_url(self):
        obj = ThingSpeakEndpoint()
        obj.configure(id=3, write_key='ZYXWVUTSRQP0987654321')

        with responses.RequestsMock() as responses_:
            responses_.add(
                    responses.GET,
                    'https://api.thingspeak.com/channels/3/feed.json',
                    json=canned_responses['https://api.thingspeak.com/channels/3/feed.json']
            )
            obj.read_config()

            assert len(responses_.calls) == 1
            the_request = responses_.calls[0].request
            assert the_request.url == 'https://api.thingspeak.com/channels/3/feed.json?results=0'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ZYXWVUTSRQP0987654321'

        assert obj.name == 'ioBridge Server'

    @responses.activate
    def test_send_data_to_url(self):
        obj = ThingSpeakEndpoint()
        obj.configure(id=3, field1='Server Temp', write_key='ZYXWVUTSRQP0987654321')

        data = {'timestamp': 1453927940, 'Server Temp': '60.0 F'}

        with responses.RequestsMock() as responses_:
            responses_.add(
                    responses.POST,
                    'https://api.thingspeak.com/update.json',
                    json=canned_responses['https://api.thingspeak.com/update.json']
            )
            obj.update(**data)

            assert len(responses_.calls) == 1
            the_request = responses_.calls[0].request
            assert the_request.url == 'https://api.thingspeak.com/update.json'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ZYXWVUTSRQP0987654321'
            assert (
                json.loads(the_request.body) ==
                {"created_at": "2016-01-27T20:52:20", "field1": "60.0 F"})


canned_responses = {
    'https://api.thingspeak.com/channels/3/feed.json': {
        "channel": {
            "id": 3,
            "name": "ioBridge Server",
            "description": "ioBridge IO-204 connected to web server to report temperatures to ThingSpeak",
            "field1": "Server Temp",
            "created_at": "2010-12-03T14:26:23Z",
            "updated_at": "2016-01-27T20:52:10Z",
            "last_entry_id": 263592
        },
        "feeds": [
            {"created_at": "2016-01-27T20:42:11Z", "entry_id": 263591, "field1": "58.3 F"},
            {"created_at": "2016-01-27T20:52:10Z", "entry_id": 263592, "field1": "58.5 F"}
        ]},
    'https://api.thingspeak.com/channels/3/feed/last.json': {
        "created_at": "2016-01-27T20:52:10Z", "entry_id": 263592, "field1": "58.5 F"
    },
    'https://api.thingspeak.com/update.json': {
        "created_at": "2016-01-27T20:52:20Z", "entry_id": 263593, "field1": "60.0 F",
        "field2": None, "field3": None, "field4": None, "field5": None, "field6": None, "field7": None, "field8": None,
    },
}
