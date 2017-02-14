import unittest.mock as mock

from sensormesh.console import ConsoleDisplay


class TestConsoleDisplay:
    def test_can_create_target(self):
        with mock.patch("builtins.print", autospec=True) as mock_print:
            t = ConsoleDisplay(name='Console Logger')
            assert not mock_print.called
            assert t.name == 'Console Logger'

    def test_update_one_value_no_timestamp(self):
        t = ConsoleDisplay()
        with mock.patch("builtins.print", autospec=True) as mock_print:
            with t:
                t.update({'value': 1})
            mock_print.assert_called_once_with('None', ':', {'value': 1})

    def test_update_one_value_with_timestamp(self):
        t = ConsoleDisplay()
        with mock.patch("builtins.print", autospec=True) as mock_print:
            with t:
                t.update({'timestamp': 1453927940, 'value': 1})
            mock_print.assert_called_once_with('2016-01-27T20:52:20', ':', {'value': 1})

    def test_update_multiple_values(self):
        t = ConsoleDisplay()
        with mock.patch("builtins.print", autospec=True) as mock_print:
            with t:
                t.update({'value1': 1, 'value2': 'kevin'})
            mock_print.assert_called_once_with('None', ':', {'value1': 1, 'value2': 'kevin'})

    def test_can_write_remote_names(self):
        t = ConsoleDisplay(
                fields=['timestamp', ('value1', 'field1')]
        )
        with mock.patch("builtins.print", autospec=True) as mock_print:
            with t:
                t.update({'value1': 1, 'value2': 'kevin'})
            mock_print.assert_called_once_with('None', ':', {'field1': 1})

    def test_can_call_multiple_times_with_timestamp(self):
        t = ConsoleDisplay()
        data = {'timestamp': 1453927940, 'value': 1}

        with mock.patch("builtins.print", autospec=True) as mock_print:
            with t:
                t.update(data)
                mock_print.assert_called_once_with('2016-01-27T20:52:20', ':', {'value': 1})

                # Check second call is not missing data
                mock_print.reset_mock()
                t.update(data)
                mock_print.assert_called_once_with('2016-01-27T20:52:20', ':', {'value': 1})
