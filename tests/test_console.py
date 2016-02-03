from unittest.mock import patch

from sensormesh.console import *


class TestConsoleDisplay:
    def test_can_create_target(self):
        with patch("builtins.print", autospec=True) as mock_print:
            t = ConsoleDisplay()
            mock_print.assert_not_called()

    def test_update_one_value_no_timestamp(self):
        t = ConsoleDisplay()
        with patch("builtins.print", autospec=True) as mock_print:
            t.update({'value': 1})
            mock_print.assert_called_once_with('None', ':', {'value': 1})

    def test_update_one_value_with_timestamp(self):
        t = ConsoleDisplay()
        with patch("builtins.print", autospec=True) as mock_print:
            t.update({'timestamp': 1453927940, 'value': 1})
            mock_print.assert_called_once_with('2016-01-27T20:52:20', ':', {'value': 1})

    def test_update_multiple_values(self):
        t = ConsoleDisplay()
        with patch("builtins.print", autospec=True) as mock_print:
            t.update({'value1': 1, 'value2': 'kevin'})
            mock_print.assert_called_once_with('None', ':', {'value1': 1, 'value2': 'kevin'})

    def test_can_call_multiple_times_with_timestamp(self):
        t = ConsoleDisplay()
        data = {'timestamp': 1453927940, 'value': 1}

        with patch("builtins.print", autospec=True) as mock_print:
            t.update(data)
            mock_print.assert_called_once_with('2016-01-27T20:52:20', ':', {'value1': 1, 'value2': 'kevin'})

            # Check second call is not missing data
            mock_print.reset_mock()
            t.update(data)
            mock_print.assert_called_once_with('2016-01-27T20:52:20', ':', {'value1': 1, 'value2': 'kevin'})
