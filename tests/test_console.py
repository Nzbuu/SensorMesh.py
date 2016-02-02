from unittest.mock import patch

from sensormesh.console import *


class TestConsoleDisplay:
    def test_can_create_target(self):
        with patch("builtins.print", autospec=True) as mock_print:
            t = ConsoleDisplay()

        assert not mock_print.called

    def test_update_one_value_no_timestamp(self):
        t = ConsoleDisplay()
        with patch("builtins.print", autospec=True) as mock_print:
            t.update({'value': 1})

        assert mock_print.call_count == 1
        assert mock_print.call_args_list[0][0] == ('None', ':', {'value': 1})

    def test_update_one_value_with_timestamp(self):
        t = ConsoleDisplay()
        with patch("builtins.print", autospec=True) as mock_print:
            t.update({'timestamp': 1453927940, 'value': 1})

        assert mock_print.call_count == 1
        assert mock_print.call_args_list[0][0] == ('2016-01-27T20:52:20', ':', {'value': 1})

    def test_update_multiple_values(self):
        t = ConsoleDisplay()
        with patch("builtins.print", autospec=True) as mock_print:
            t.update({'value1': 1, 'value2': 'kevin'})

        assert mock_print.call_count == 1
        assert mock_print.call_args_list[0][0] == ('None', ':', {'value1': 1, 'value2': 'kevin'})

    def test_can_call_multiple_times_with_timestamp(self):
        t = ConsoleDisplay()
        data = {'timestamp': 1453927940, 'value': 1}

        with patch("builtins.print", autospec=True) as mock_print:
            t.update(data)
            t.update(data)

        assert mock_print.call_count == 2
        assert mock_print.call_args_list[0][0] == ('2016-01-27T20:52:20', ':', {'value': 1})
        assert mock_print.call_args_list[1][0] == ('2016-01-27T20:52:20', ':', {'value': 1})  # Second call not missing data
