import unittest.mock as mock

import responses
import pytest

from sensormesh.twitter import TwitterApi, TwitterUpdate


class TestTwitterApi:
    @mock.patch('tweepy.API')
    @mock.patch('tweepy.OAuthHandler')
    def test_calls_api_to_update_status(self, mock_auth, mock_api):
        with responses.RequestsMock() as r_mock:
            api = TwitterApi()
            api.post_update({'message': 'This is a status update!', 'string': 'This is ignored'})

        api._api.update_status.assert_called_with(status='This is a status update!')
        assert not r_mock.calls


class TestTwitterUpdate:
    def test_cannot_create_without_api(self):
        with pytest.raises(ValueError):
            _ = TwitterUpdate(name='Test Logger')

    def test_can_create_with_empty_api(self):
        with pytest.raises(ValueError):
            _ = TwitterUpdate(api=None, name='Alt Logger')

    def test_can_inject_api(self):
        api = mock.MagicMock(spec=TwitterApi)
        obj = TwitterUpdate(api=api)
        assert obj._api is api

    def test_can_update_with_api(self):
        mock_api = mock.MagicMock(spec=TwitterApi)

        obj = TwitterUpdate(
            api=mock_api,
            message='The temperature is {field1}',
            fields=[
                ('Server Temp', 'field1'),
                ('timestamp', 'created_at'),
            ]
        )

        data = {
            'timestamp': 1453927940,
            'Server Temp': '60.0 F',
        }
        with obj:
            obj.update(data)

        data_out = {
            'created_at': 1453927940,
            'field1': '60.0 F',
            'message': 'The temperature is 60.0 F'
        }

        assert mock_api.post_update.call_count == 1
        mock_api.post_update.assert_called_with(data_out)
