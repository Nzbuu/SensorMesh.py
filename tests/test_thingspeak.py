import json
import unittest.mock as mock

import pytest
import responses
import requests.exceptions

from sensormesh.thingspeak import (
    ThingSpeakApi, ThingSpeakLogger, ThingSpeakSource, ConfigurationError)


class TestThingSpeakSource:
    def test_cannot_create_source_without_api(self):
        with pytest.raises(ValueError):
            _ = ThingSpeakSource(name='Test Source')

    def test_cannot_create_source_with_empty_api(self):
        with pytest.raises(ValueError):
            _ = ThingSpeakSource(api=None, name='Alt Source')

    def test_can_configure_key(self):
        obj = ThingSpeakSource(api={'key': 'ABCDEFGHIJKLMNOPQRST'})
        assert obj._api.key == 'ABCDEFGHIJKLMNOPQRST'

    def test_can_configure_channel(self):
        obj = ThingSpeakSource(api={'channel': 3})
        assert obj._api.channel == 3

    def test_can_inject_api(self):
        api = mock.MagicMock(spec=ThingSpeakApi)
        obj = ThingSpeakSource(api=api)
        assert obj._api is api

    def test_can_read_with_api(self):
        mock_api = mock.MagicMock(spec=ThingSpeakApi)
        mock_api.get_data.return_value = canned_responses['last.json']

        obj = ThingSpeakSource(
            api=mock_api,
            fields=[
                ('Server Temp', 'field1'),
                ('timestamp', 'created_at')
            ]
        )

        with obj:
            data = obj.read()

        assert mock_api.get_data.call_count == 1
        mock_api.get_data.assert_called_with()

        assert data == {
            'timestamp': 1453927930,
            'Server Temp': '58.5 F',
        }


class TestThingSpeakLogger:
    def test_cannot_create_logger_without_api(self):
        with pytest.raises(ValueError):
            _ = ThingSpeakLogger(name='Test Logger')

    def test_can_create_logger_with_empty_api(self):
        with pytest.raises(ValueError):
            _ = ThingSpeakLogger(api=None, name='Alt Logger')

    def test_can_configure_key(self):
        obj = ThingSpeakLogger(api={'key': 'ZYXWVUTSRQP0987654321'}, name='Test Logger')
        assert obj._api.key == 'ZYXWVUTSRQP0987654321'

    def test_can_inject_api(self):
        api = mock.MagicMock(spec=ThingSpeakApi)
        obj = ThingSpeakLogger(api=api)
        assert obj._api is api

    def test_can_update_with_api(self):
        mock_api = mock.MagicMock()
        mock_api.post_update.return_value = canned_responses['update.json']

        obj = ThingSpeakLogger(
            api=mock_api,
            fields=[
                ('Server Temp', 'field1'),
                ('timestamp', 'created_at')
            ]
        )

        data = {
            'timestamp': 1453927940,
            'Server Temp': '60.0 F',
        }
        with obj:
            obj.update(data)

        assert mock_api.post_update.call_count == 1
        mock_api.post_update.assert_called_with({
            "created_at": "2016-01-27T20:52:20", "field1": "60.0 F"})


class TestThingSpeakApi:
    def test_default_properties(self):
        api = ThingSpeakApi()
        assert api.base_url == 'https://api.thingspeak.com'
        assert api.key is None
        assert api.channel is None

    def test_can_configure_properties(self):
        api = ThingSpeakApi(
            key='ABCDEFGHIJ1234567890',
            channel=700,
            base_url='https://api.example.com:6666'
        )
        assert api.base_url == 'https://api.example.com:6666'
        assert api.key == 'ABCDEFGHIJ1234567890'
        assert api.channel == 700

    def test_url_for_update(self):
        api = ThingSpeakApi(
            key='ABCDEFGHIJ1234567890',
            channel=700,
            base_url='https://api.example.com:6666'
        )
        assert (api._get_url('update') ==
                'https://api.example.com:6666/update.json')

    def test_url_for_last(self):
        api = ThingSpeakApi(
            key='ABCDEFGHIJ1234567890',
            channel=700,
            base_url='https://api.example.com:6666'
        )
        assert (api._get_url('last') ==
                'https://api.example.com:6666/channels/700/feed/last.json')

    def test_can_get_data_with_url(self):
        api = ThingSpeakApi(
            key='ABCDEFGHIJKLMNOPQRST',
            channel=666,
            base_url='https://api.example.com:6666'
        )

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                r_mock.GET,
                'https://api.example.com:6666/channels/666/feed/last.json',
                json=canned_responses['last.json']
            )
            data = api.get_data()

            assert len(r_mock.calls) == 1
            the_request = r_mock.calls[0].request
            assert the_request.url == 'https://api.example.com:6666/channels/666/feed/last.json'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ABCDEFGHIJKLMNOPQRST'

        assert data['created_at'] == '2016-01-27T20:52:10Z'
        assert data['field1'] == '58.5 F'

    def test_cannot_get_data_without_channel(self):
        api = ThingSpeakApi(
            key='ABCDEFGHIJKLMNOPQRST',
            base_url='https://api.example.com:6666'
        )

        with responses.RequestsMock() as r_mock, \
                pytest.raises(ConfigurationError):
            data = api.get_data()

        assert len(r_mock.calls) == 0

    def test_can_get_data_without_key(self):
        api = ThingSpeakApi(
            channel=666,
            base_url='https://api.example.com:6666'
        )

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                r_mock.GET,
                'https://api.example.com:6666/channels/666/feed/last.json',
                json=canned_responses['last.json']
            )
            data = api.get_data()

            assert len(r_mock.calls) == 1
            the_request = r_mock.calls[0].request
            assert the_request.url == 'https://api.example.com:6666/channels/666/feed/last.json'
            assert 'X-THINGSPEAKAPIKEY' not in the_request.headers

        assert data['created_at'] == '2016-01-27T20:52:10Z'
        assert data['field1'] == '58.5 F'

    def test_get_data_connection_error(self):
        api = ThingSpeakApi(
            channel=666,
            base_url='https://api.example.com:6666'
        )

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                r_mock.GET,
                'https://api.example.com:6666/channels/666/feed/last.json',
                body=requests.exceptions.ConnectionError()
            )

            with pytest.raises(requests.exceptions.ConnectionError):
                _ = api.get_data()

            assert len(r_mock.calls) == 1
            assert r_mock.calls[0].request.url == 'https://api.example.com:6666/channels/666/feed/last.json'
            assert type(r_mock.calls[0].response) is requests.exceptions.ConnectionError

    def test_can_post_update_with_url(self):
        api = ThingSpeakApi(
            key='ZYXWVUTSRQP0987654321',
            channel=666,
            base_url='https://api.example.com:6666'
        )
        data = {"created_at": "2016-01-27T20:52:20", "field1": "60.0 F"}

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                r_mock.POST,
                'https://api.example.com:6666/update.json',
                json=canned_responses['update.json']
            )
            api.post_update(data)

            assert len(r_mock.calls) == 1
            the_request = r_mock.calls[0].request
            assert the_request.url == 'https://api.example.com:6666/update.json'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ZYXWVUTSRQP0987654321'
            assert json.loads(the_request.body) == data

    def test_can_post_update_without_channel(self):
        api = ThingSpeakApi(
            key='ZYXWVUTSRQP0987654321',
            base_url='https://api.example.com:6666'
        )
        data = {"created_at": "2016-01-27T20:52:20", "field1": "60.0 F"}

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                r_mock.POST,
                'https://api.example.com:6666/update.json',
                json=canned_responses['update.json']
            )
            api.post_update(data)

            assert len(r_mock.calls) == 1
            the_request = r_mock.calls[0].request
            assert the_request.url == 'https://api.example.com:6666/update.json'
            assert the_request.headers['X-THINGSPEAKAPIKEY'] == 'ZYXWVUTSRQP0987654321'
            assert json.loads(the_request.body) == data

    def test_cannot_post_update_without_key(self):
        api = ThingSpeakApi(
            channel=666,
            base_url='https://api.example.com:6666'
        )
        data = {"created_at": "2016-01-27T20:52:20", "field1": "60.0 F"}

        with responses.RequestsMock() as r_mock, \
                pytest.raises(ConfigurationError):
            api.post_update(data)

        assert len(r_mock.calls) == 0

    def test_post_update_connection_error(self):
        api = ThingSpeakApi(
            key='ZYXWVUTSRQP0987654321',
            base_url='https://api.example.com:6666'
        )
        data = {"created_at": "2016-01-27T20:52:20", "field1": "60.0 F"}

        with responses.RequestsMock() as r_mock:
            r_mock.add(
                r_mock.POST,
                'https://api.example.com:6666/update.json',
                body=requests.exceptions.ConnectionError()
            )

            with pytest.raises(requests.exceptions.ConnectionError):
                api.post_update(data)

            assert len(r_mock.calls) == 1
            assert r_mock.calls[0].request.url == 'https://api.example.com:6666/update.json'
            assert type(r_mock.calls[0].response) is requests.exceptions.ConnectionError


canned_responses = {
    'last.json': {
        "created_at": "2016-01-27T20:52:10Z", "entry_id": 263592, "field1": "58.5 F"
    },
    'update.json': {
        "created_at": "2016-01-27T20:52:20Z", "entry_id": 263593,
        "field1": "60.0 F", "field2": None, "field3": None, "field4": None,
        "field5": None, "field6": None, "field7": None, "field8": None,
    },
}
