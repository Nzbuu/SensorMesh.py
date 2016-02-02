import pytest
import responses

from sensormesh.thingspeak import *


class TestThingSpeakSource:
    def test_can_create_source(self):
        obj = ThingSpeakSource(name='Test Source')
        assert obj.name == 'Test Source'

    def test_default_key_is_none(self):
        obj = ThingSpeakSource()
        assert obj._api._get_key(write=False) is None

    def test_can_configure_key(self):
        obj = ThingSpeakSource(
                key='ABCDEFGHIJKLMNOPQRST'
        )
        assert obj._api._get_key(write=False) == 'ABCDEFGHIJKLMNOPQRST'

    @responses.mock.activate
    def test_can_read_data_from_url(self):
        obj = ThingSpeakSource(
                channel=3,
                key='ABCDEFGHIJKLMNOPQRST',
                feeds={'field1': 'Server Temp'}
        )

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                    r_mock.GET,
                    'https://api.thingspeak.com/channels/3/feed/last.json',
                    json=canned_responses['https://api.thingspeak.com/channels/3/feed/last.json']
            )
            data = obj.read()

            assert len(r_mock.calls) == 1
            the_request = r_mock.calls[0].request
            assert the_request.url == 'https://api.thingspeak.com/channels/3/feed/last.json'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ABCDEFGHIJKLMNOPQRST'

        assert data['timestamp'] == 1453927930
        assert data['Server Temp'] == '58.5 F'

    @responses.mock.activate
    def test_can_read_data_without_key(self):
        obj = ThingSpeakSource(
                channel=3,
                feeds={'field1': 'Server Temp'}
        )

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                    r_mock.GET,
                    'https://api.thingspeak.com/channels/3/feed/last.json',
                    json=canned_responses['https://api.thingspeak.com/channels/3/feed/last.json']
            )
            data = obj.read()

            assert len(r_mock.calls) == 1
            the_request = r_mock.calls[0].request
            assert the_request.url == 'https://api.thingspeak.com/channels/3/feed/last.json'
            assert 'X-THINGSPEAKAPIKEY' not in the_request.headers

        assert data['timestamp'] == 1453927930
        assert data['Server Temp'] == '58.5 F'


class TestThingSpeakLogger:
    def test_can_create_logger(self):
        obj = ThingSpeakLogger(name='Test Logger')
        assert obj.name == 'Test Logger'

    def test_no_key_is_error(self):
        obj = ThingSpeakLogger()
        with pytest.raises(ConfigurationError):
            obj._api._get_key(write=True)

    def test_can_configure_key(self):
        obj = ThingSpeakLogger(key='ZYXWVUTSRQP0987654321')
        assert obj._api._get_key(write=True) == 'ZYXWVUTSRQP0987654321'

    @responses.mock.activate
    def test_send_data_to_url(self):
        obj = ThingSpeakLogger(
                channel=3,
                key='ZYXWVUTSRQP0987654321',
                feeds={'field1': 'Server Temp'}
        )

        data = {'timestamp': 1453927940, 'Server Temp': '60.0 F'}

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                    r_mock.POST,
                    'https://api.thingspeak.com/update.json',
                    json=canned_responses['https://api.thingspeak.com/update.json']
            )
            obj.update(data)

            assert len(r_mock.calls) == 1
            the_request = r_mock.calls[0].request
            assert the_request.url == 'https://api.thingspeak.com/update.json'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ZYXWVUTSRQP0987654321'
            assert (
                json.loads(the_request.body) ==
                {"created_at": "2016-01-27T20:52:20", "field1": "60.0 F"})


canned_responses = {
    'https://api.thingspeak.com/channels/3/feed/last.json': {
        "created_at": "2016-01-27T20:52:10Z", "entry_id": 263592, "field1": "58.5 F"
    },
    'https://api.thingspeak.com/update.json': {
        "created_at": "2016-01-27T20:52:20Z", "entry_id": 263593, "field1": "60.0 F",
        "field2": None, "field3": None, "field4": None, "field5": None, "field6": None, "field7": None, "field8": None,
    },
}
