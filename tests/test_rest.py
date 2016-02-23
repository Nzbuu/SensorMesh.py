import unittest.mock as mock
import logging

import pytest
import testfixtures

from sensormesh.rest import RestSource, RestTarget, RestApi, ApiMixin


class TestRestSource:
    def test_cannot_create_source_without_api(self):
        with pytest.raises(ValueError):
            _ = RestSource()

    def test_cannot_create_source_with_empty_api(self):
        with pytest.raises(ValueError):
            _ = RestSource(api=None)

    def test_can_create_with_api(self):
        mock_api = mock.MagicMock()
        o = RestSource(api=mock_api, name='REST server')
        assert o._api is mock_api
        assert o.name == 'REST server'

    def test_can_read_with_fields(self):
        mock_api = mock.MagicMock()
        mock_api.get_data.return_value = {'field1': 1}
        o = RestSource(api=mock_api, fields=[('valueX', 'field1')])
        with o:
            data = o.read()
        mock_api.get_data.assert_called_with()
        assert data == {'valueX': 1}

    def test_can_read_without_fields(self):
        mock_api = mock.MagicMock()
        mock_api.get_data.return_value = {'valueY': 1}
        o = RestSource(api=mock_api)
        with o:
            data = o.read()
        mock_api.get_data.assert_called_with()
        assert data == {'valueY': 1}

    def test_can_read_with_missing_inputs(self):
        mock_api = mock.MagicMock()
        mock_api.get_data.return_value = {'field1': 1}
        o = RestSource(api=mock_api, fields=[('valueX', 'field1'), ('count', 'field2')])
        with o:
            data = o.read()
        mock_api.get_data.assert_called_with()
        assert data == {'valueX': 1}

    def test_can_read_with_extra_inputs(self):
        mock_api = mock.MagicMock()
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
        mock_api = mock.MagicMock()
        o = RestTarget(api=mock_api, name='REST server')
        assert o._api is mock_api
        assert o.name == 'REST server'

    def test_can_update_with_fields(self):
        mock_api = mock.MagicMock()
        o = RestTarget(api=mock_api, fields=[('value', 'field1')])
        with o:
            o.update({'value': 1})
        mock_api.post_update.assert_called_with({'field1': 1})

    def test_can_update_without_fields(self):
        mock_api = mock.MagicMock()
        o = RestTarget(api=mock_api)
        with o:
            o.update({'value': 1})
        mock_api.post_update.assert_called_with({'value': 1})

    def test_can_update_with_missing_inputs(self):
        mock_api = mock.MagicMock()
        o = RestTarget(api=mock_api, fields=[('value', 'field1'), ('count', 'field2')])
        with o:
            o.update({'value': 1})
        mock_api.post_update.assert_called_with({'field1': 1})

    def test_can_update_with_extra_inputs(self):
        mock_api = mock.MagicMock()
        o = RestTarget(api=mock_api, fields=[('value', 'field1')])
        with o:
            o.update({'value': 1, 'other': 0})
        mock_api.post_update.assert_called_with({'field1': 1})


class TestApiMixin:
    def test_can_use_object_as_context_manager(self):
        mock_api = RestApi()
        obj = ApiMixin(api=mock_api, name='mock_obj')

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            with obj as context:
                # Check that context is the same object
                assert context is obj

                assert len(l.records) == 2
                assert_record_is(l.records[0], 'INFO', "Opening ApiMixin(name='mock_obj')")
                assert_record_is(l.records[1], 'INFO', "Opening RestApi()")

        assert len(l.records) == 4
        assert_record_is(l.records[2], 'INFO', "Closing RestApi()")
        assert_record_is(l.records[3], 'INFO', "Closing ApiMixin(name='mock_obj')")

    def test_can_open_and_close_object(self):
        mock_api = RestApi()
        obj = ApiMixin(api=mock_api, name='mock_obj')

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            obj.open()
            assert len(l.records) == 2
            assert_record_is(l.records[0], 'INFO', "Opening ApiMixin(name='mock_obj')")
            assert_record_is(l.records[1], 'INFO', "Opening RestApi()")

            obj.close()
            assert len(l.records) == 4
            assert_record_is(l.records[2], 'INFO', "Closing RestApi()")
            assert_record_is(l.records[3], 'INFO', "Closing ApiMixin(name='mock_obj')")


def assert_record_is(record, level, message):
    assert record.levelname == level
    assert record.getMessage() == message
