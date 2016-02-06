import unittest.mock as mock

import pytest

from sensormesh.text import *


class TestTextLogger:
    def test_cannot_create_without_filename(self):
        with pytest.raises(TypeError):
            _ = TextLogger(feeds=['timestamp', 'values'])

    def test_cannot_create_without_feeds(self):
        with pytest.raises(TypeError):
            _ = TextLogger(filename='temp_logfile.txt')

    def test_can_create_with_filename(self):
        l = TextLogger(
                filename='temp_logfile.txt',
                name='CsvLogger',
                feeds=['timestamp', 'values']
        )
        assert l.name == 'CsvLogger'
        assert l.filename == 'temp_logfile.txt'
        assert l.fields == ['timestamp', 'values']

    def test_can_start_new_file(self):
        mock_isfile = mock.Mock(return_value=False)
        mock_file = mock.mock_open()

        with mock.patch('os.path.isfile', mock_isfile):
            with mock.patch('builtins.open', mock_file):
                o = TextLogger(
                        filename='temp_file.txt',
                        feeds=['timestamp', 'value']
                )
                data = {'timestamp': 100, 'value': 200}
                o.update(data)

        assert mock_isfile.call_count == 1

        assert mock_file.call_count == 1
        mock_file.assert_called_with('temp_file.txt', 'a')

        file_handle = mock_file()
        assert file_handle.write.call_count == 2
        file_handle.write.assert_has_calls([
            mock.call('timestamp,value\r\n'),
            mock.call('100,200\r\n'),
        ])

    def test_can_continue_existing_file(self):
        mock_isfile = mock.Mock(return_value=True)
        mock_file = mock.mock_open()

        with mock.patch('os.path.isfile', mock_isfile):
            with mock.patch('builtins.open', mock_file):
                o = TextLogger(
                        filename='temp_file.txt',
                        feeds=['timestamp', 'value']
                )
                data = {'timestamp': 150, 'value': 250}
                o.update(data)

        assert mock_isfile.call_count == 1

        assert mock_file.call_count == 1
        mock_file.assert_called_with('temp_file.txt', 'a')

        file_handle = mock_file()
        assert file_handle.write.call_count == 1
        file_handle.write.assert_called_with('150,250\r\n')
