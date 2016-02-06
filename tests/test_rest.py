import unittest.mock as mock

import pytest

from sensormesh.rest import *


class TestRestTarget:
    def test_cannot_create_target_without_api(self):
        with pytest.raises(ConfigurationError):
            o = RestTarget()

    def test_can_create_with_api(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api, name='REST server')
        assert o._api is mock_api
        assert o.name == 'REST server'

    def test_can_update_with_feeds(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api, feeds={'field1': 'value'})
        o.update({'value': 1})
        mock_api.post_update.assert_called_with({'field1': 1})

    def test_can_update_without_feeds(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api)
        o.update({'value': 1})
        mock_api.post_update.assert_called_with({'value': 1})

    def test_can_update_with_missing_inputs(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api, feeds={'field1': 'value', 'field2': 'count'})
        o.update({'value': 1})
        mock_api.post_update.assert_called_with({'field1': 1})

    def test_can_update_with_extra_inputs(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api, feeds={'field1': 'value'})
        o.update({'value': 1, 'other': 0})
        mock_api.post_update.assert_called_with({'field1': 1})
