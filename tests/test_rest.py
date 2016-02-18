import unittest.mock as mock

import pytest

from sensormesh.rest import RestSource, RestTarget


class TestRestSource:
    def test_cannot_create_source_without_api(self):
        with pytest.raises(ValueError):
            _ = RestSource()

    def test_cannot_create_source_with_empty_api(self):
        with pytest.raises(ValueError):
            _ = RestSource(api=None)

    def test_can_create_with_api(self):
        mock_api = mock.Mock()
        o = RestSource(api=mock_api, name='REST server')
        assert o._api is mock_api
        assert o.name == 'REST server'

    def test_can_read_with_fields(self):
        mock_api = mock.Mock()
        mock_api.get_data.return_value = {'field1': 1}
        o = RestSource(api=mock_api, fields=[('valueX', 'field1')])
        with o:
            data = o.read()
        mock_api.get_data.assert_called_with()
        assert data == {'valueX': 1}

    def test_can_read_without_fields(self):
        mock_api = mock.Mock()
        mock_api.get_data.return_value = {'valueY': 1}
        o = RestSource(api=mock_api)
        with o:
            data = o.read()
        mock_api.get_data.assert_called_with()
        assert data == {'valueY': 1}

    def test_can_read_with_missing_inputs(self):
        mock_api = mock.Mock()
        mock_api.get_data.return_value = {'field1': 1}
        o = RestSource(api=mock_api, fields=[('valueX', 'field1'), ('count', 'field2')])
        with o:
            data = o.read()
        mock_api.get_data.assert_called_with()
        assert data == {'valueX': 1}

    def test_can_read_with_extra_inputs(self):
        mock_api = mock.Mock()
        mock_api.get_data.return_value = {'field1': 1, 'field2': 2}
        o = RestSource(api=mock_api, fields=[('valueX', 'field1')])
        with o:
            data = o.read()
        mock_api.get_data.assert_called_with()
        assert data == {'valueX': 1}



class TestRestTarget:
    def test_cannot_create_target_without_api(self):
        with pytest.raises(ValueError):
            o = RestTarget()

    def test_cannot_create_target_with_empty_api(self):
        with pytest.raises(ValueError):
            o = RestTarget(api=None)

    def test_can_create_with_api(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api, name='REST server')
        assert o._api is mock_api
        assert o.name == 'REST server'

    def test_can_update_with_fields(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api, fields=[('value', 'field1')])
        with o:
            o.update({'value': 1})
        mock_api.post_update.assert_called_with({'field1': 1})

    def test_can_update_without_fields(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api)
        with o:
            o.update({'value': 1})
        mock_api.post_update.assert_called_with({'value': 1})

    def test_can_update_with_missing_inputs(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api, fields=[('value', 'field1'), ('count', 'field2')])
        with o:
            o.update({'value': 1})
        mock_api.post_update.assert_called_with({'field1': 1})

    def test_can_update_with_extra_inputs(self):
        mock_api = mock.Mock()
        o = RestTarget(api=mock_api, fields=[('value', 'field1')])
        with o:
            o.update({'value': 1, 'other': 0})
        mock_api.post_update.assert_called_with({'field1': 1})
