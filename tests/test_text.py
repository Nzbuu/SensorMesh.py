import unittest.mock as mock

import pytest
import testfixtures

from sensormesh.text import *


class TestTextLogger:
    def test_cannot_create_without_filename(self):
        with pytest.raises(TypeError):
            _ = TextLogger(fields=['timestamp', 'values'])

    def test_cannot_create_without_fields(self):
        with pytest.raises(TypeError):
            _ = TextLogger(filename='temp_logfile.txt')

    def test_string_includes_name_and_filename(self):
        t = TextLogger(name="csv_file", filename='temp_logfile.txt', mode='w', fields=['value'])
        assert str(t) == "TextLogger(name='csv_file', filename='temp_logfile.txt')"

    def test_default_mode_is_append(self):
        t = TextLogger(filename='temp_logfile.txt', fields=['value'])
        assert t.mode == 'a'

    def test_requires_valid_mode(self):
        with pytest.raises(ValueError):
            _ = TextLogger(
                filename='temp_logfile.txt',
                mode='x',
                fields=['value']
            )

    def test_can_create_with_filename(self):
        l = TextLogger(
            filename='temp_logfile.txt',
            name='CsvLogger',
            fields=['timestamp', 'values']
        )
        assert l.name == 'CsvLogger'
        assert l.filename == 'temp_logfile.txt'
        assert l.fields == ['timestamp', 'values']

    def test_can_start_new_file(self):
        mock_isfile = mock.Mock(return_value=False)
        mock_file = mock.mock_open()

        with mock.patch('os.path.isfile', mock_isfile), \
             mock.patch('builtins.open', mock_file), \
             testfixtures.LogCapture(level=logging.INFO) as logs:
            o = TextLogger(
                filename='temp_file.txt',
                mode='a',
                fields=['timestamp', 'value']
            )
            data = {'timestamp': 100, 'value': 200}
            with o:
                o.update(data)

        assert mock_isfile.call_count == 1

        assert mock_file.call_count == 1
        mock_file.assert_called_with('temp_file.txt', 'a', newline='')

        file_handle = mock_file()
        assert file_handle.write.call_count == 2
        file_handle.write.assert_has_calls([
            mock.call('timestamp,value\r\n'),
            mock.call('100,200\r\n'),
        ])

        assert len(logs.records) == 4
        assert_record_is(logs.records[0], 'INFO', "Opening TextLogger(name='', filename='temp_file.txt')")
        assert_record_is(logs.records[1], 'INFO',
                         "Creating 'temp_file.txt' for TextLogger(name='', filename='temp_file.txt')")
        assert_record_is(logs.records[2], 'INFO', "Updating TextLogger(name='', filename='temp_file.txt')")
        assert_record_is(logs.records[3], 'INFO', "Closing TextLogger(name='', filename='temp_file.txt')")

    def test_can_continue_existing_file(self):
        mock_isfile = mock.Mock(return_value=True)
        mock_file = mock.mock_open()

        with mock.patch('os.path.isfile', mock_isfile), \
             mock.patch('builtins.open', mock_file), \
             testfixtures.LogCapture(level=logging.INFO) as logs:
            o = TextLogger(
                filename='temp_file.txt',
                mode='a',
                fields=['timestamp', 'value']
            )
            data = {'timestamp': 150, 'value': 250}
            with o:
                o.update(data)

        assert mock_isfile.call_count == 1

        assert mock_file.call_count == 1
        mock_file.assert_called_with('temp_file.txt', 'a', newline='')

        file_handle = mock_file()
        assert file_handle.write.call_count == 1
        file_handle.write.assert_called_with('150,250\r\n')

        assert len(logs.records) == 3
        assert_record_is(logs.records[0], 'INFO', "Opening TextLogger(name='', filename='temp_file.txt')")
        assert_record_is(logs.records[1], 'INFO', "Updating TextLogger(name='', filename='temp_file.txt')")
        assert_record_is(logs.records[2], 'INFO', "Closing TextLogger(name='', filename='temp_file.txt')")

    def test_can_write_remote_names(self):
        mock_isfile = mock.Mock(return_value=False)
        mock_file = mock.mock_open()

        with mock.patch('os.path.isfile', mock_isfile), \
             mock.patch('builtins.open', mock_file):
            o = TextLogger(
                filename='temp_file.txt',
                mode='w',
                fields=['timestamp', ('value', 'field1')]
            )
            data = {'timestamp': 110, 'value': 210}
            with o:
                o.update(data)

        # Doesn't matter if this is called since want to overwrite anyway
        assert mock_isfile.call_count in {0, 1}

        assert mock_file.call_count == 1
        mock_file.assert_called_with('temp_file.txt', 'w', newline='')

        file_handle = mock_file()
        assert file_handle.write.call_count == 2
        file_handle.write.assert_has_calls([
            mock.call('timestamp,field1\r\n'),
            mock.call('110,210\r\n'),
        ])

    def test_ignores_extra_inputs(self):
        mock_isfile = mock.Mock(return_value=False)
        mock_file = mock.mock_open()

        with mock.patch('os.path.isfile', mock_isfile), \
             mock.patch('builtins.open', mock_file):
            o = TextLogger(
                filename='temp_file.txt',
                mode='w',
                fields=['timestamp', 'value']
            )
            data = {'timestamp': 1100, 'value': 2100}
            with o:
                o.update(data)

        # Doesn't matter if this is called since want to overwrite anyway
        assert mock_isfile.call_count in {0, 1}

        assert mock_file.call_count == 1
        mock_file.assert_called_with('temp_file.txt', 'w', newline='')

        file_handle = mock_file()
        assert file_handle.write.call_count == 2
        file_handle.write.assert_has_calls([
            mock.call('timestamp,value\r\n'),
            mock.call('1100,2100\r\n'),
        ])

    def test_create_missing_inputs(self):
        mock_isfile = mock.Mock(return_value=False)
        mock_file = mock.mock_open()

        with mock.patch('os.path.isfile', mock_isfile), \
             mock.patch('builtins.open', mock_file):
            o = TextLogger(
                filename='temp_file.txt',
                mode='w',
                fields=['timestamp', 'r1', 'r2']
            )
            data = {'timestamp': 1200, 'r2': 5}
            with o:
                o.update(data)

        # Doesn't matter if this is called since want to overwrite anyway
        assert mock_isfile.call_count in {0, 1}

        assert mock_file.call_count == 1
        mock_file.assert_called_with('temp_file.txt', 'w', newline='')

        file_handle = mock_file()
        assert file_handle.write.call_count == 2
        file_handle.write.assert_has_calls([
            mock.call('timestamp,r1,r2\r\n'),
            mock.call('1200,,5\r\n'),
        ])


def assert_record_is(record, level, message):
    assert record.levelname == level
    assert record.getMessage() == message
