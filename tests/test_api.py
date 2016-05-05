import logging

import testfixtures

from sensormesh.endpoints import DataApi, ApiMixin


class TestApiMixin:
    def test_can_use_object_as_context_manager(self):
        mock_api = DataApi()
        obj = ApiMixin(api=mock_api, name='mock_obj')

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            with obj as context:
                # Check that context is the same object
                assert context is obj

                assert len(l.records) == 2
                assert_record_is(l.records[0], 'INFO', "Opening ApiMixin(name='mock_obj')")
                assert_record_is(l.records[1], 'INFO', "Opening DataApi()")

        assert len(l.records) == 4
        assert_record_is(l.records[2], 'INFO', "Closing DataApi()")
        assert_record_is(l.records[3], 'INFO', "Closing ApiMixin(name='mock_obj')")

    def test_can_open_and_close_object(self):
        mock_api = DataApi()
        obj = ApiMixin(api=mock_api, name='mock_obj')

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            obj.open()
            assert len(l.records) == 2
            assert_record_is(l.records[0], 'INFO', "Opening ApiMixin(name='mock_obj')")
            assert_record_is(l.records[1], 'INFO', "Opening DataApi()")

            obj.close()
            assert len(l.records) == 4
            assert_record_is(l.records[2], 'INFO', "Closing DataApi()")
            assert_record_is(l.records[3], 'INFO', "Closing ApiMixin(name='mock_obj')")


def assert_record_is(record, level, message):
    assert record.levelname == level
    assert record.getMessage() == message
