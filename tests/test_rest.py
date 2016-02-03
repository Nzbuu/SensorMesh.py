from unittest.mock import Mock

import pytest

from sensormesh.rest import *


class TestRestTarget:
    def test_can_create_target_without_api(self):
        o = RestTarget(name='REST server')
        assert o.name == 'REST server'
        assert o._api is None

    def test_can_create_with_api(self):
        mock_api = Mock()
        o = RestTarget(api=mock_api)
        assert o._api is mock_api

    def test_update_without_api_throws(self):
        o = RestTarget()
        with pytest.raises(ConfigurationError):
            o.update({'value': 1})

    def test_can_update_with_api(self):
        mock_api = Mock()
        o = RestTarget(api=mock_api)
        o.update({'value': 1})
        mock_api.post_update.assert_called_with({'value': 1})
