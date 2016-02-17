import unittest.mock as mock
import logging

import pytest
import testfixtures

from sensormesh.application import *
from sensormesh.endpoints import DataSource, DataTarget


class TestController:
    def test_can_create_app(self):
        a = Controller()

    def test_can_add_source(self):
        a = Controller()
        s = mock_source('Mock Source')
        a.add_source(s)
        assert a.get_source_names() == ('Mock Source',)

    def test_can_add_2_sources(self):
        a = Controller()
        s1 = mock_source('Source 1')
        s2 = mock_source('Source 2')
        a.add_source(s1)
        a.add_source(s2)
        assert a.get_source_names() == ('Source 1', 'Source 2')

    def test_can_add_target(self):
        a = Controller()
        t = mock_target('Mock Target')
        a.add_target(t)
        assert a.get_target_names() == ('Mock Target',)

    def test_can_add_2_targets(self):
        a = Controller()
        t1 = mock_target('Mock Target 1')
        t2 = mock_target('Mock Target 2')
        a.add_target(t1)
        a.add_target(t2)
        assert a.get_target_names() == ('Mock Target 1', 'Mock Target 2')

    def test_cannot_start_without_target(self):
        a = Controller()
        s = mock_source()
        a.add_source(s)
        with pytest.raises(ConfigurationError):
            a.run()

    def test_cannot_start_without_source(self):
        a = Controller()
        t = mock_target()
        a.add_target(t)
        with pytest.raises(ConfigurationError):
            a.run()

    def test_runs_with_zero_step(self):
        a = mock_application()
        a._trigger._timefcn.side_effect = [1453928000, 1453928000.1, 1453928000.2]
        a.set_steps(time_step=0, num_steps=2)
        a._step = mock.Mock()

        with testfixtures.LogCapture(level=logging.WARNING) as l_warn:
            a.run()

        assert a._step.call_count == 2
        assert a._trigger._delayfcn.call_count == 0  # Never sleeps

        # All resources started
        assert a._sources[0].open.call_count == 1
        assert a._targets[0].open.call_count == 1
        assert a._targets[1].open.call_count == 1

        # All resources stopped
        assert a._sources[0].close.call_count == 1
        assert a._targets[0].close.call_count == 1
        assert a._targets[1].close.call_count == 1

        # No events logged
        assert not l_warn.records

    def test_runs_with_nonzero_step(self):
        a = mock_application()
        a._trigger._timefcn.side_effect = [1453928000, 1453928000.1, 1453928001.1]
        a.set_steps(time_step=1, num_steps=2)
        a._step = mock.Mock()

        with testfixtures.LogCapture(level=logging.WARNING) as l_warn:
            a.run()

        assert a._step.call_count == 2
        assert a._trigger._delayfcn.call_count == 1  # Don't delay after final step

        # All resources started
        assert a._sources[0].open.call_count == 1
        assert a._targets[0].open.call_count == 1
        assert a._targets[1].open.call_count == 1

        # All resources stopped
        assert a._sources[0].close.call_count == 1
        assert a._targets[0].close.call_count == 1
        assert a._targets[1].close.call_count == 1

        # No events logged
        assert not l_warn.records

    def test_skips_missing_steps(self):
        a = mock_application()
        a._trigger._timefcn.side_effect = [1453928000, 1453928001.1, 1453928003.1]
        a.set_steps(time_step=1, num_steps=2)
        a._step = mock.Mock()

        with testfixtures.LogCapture(level=logging.WARNING) as l_warn:
            a.run()

        assert a._step.call_count == 2
        assert a._trigger._delayfcn.call_count == 1  # Don't delay after final step

        # All resources started
        assert a._sources[0].open.call_count == 1
        assert a._targets[0].open.call_count == 1
        assert a._targets[1].open.call_count == 1

        # All resources stopped
        assert a._sources[0].close.call_count == 1
        assert a._targets[0].close.call_count == 1
        assert a._targets[1].close.call_count == 1

        # No events logged
        assert not l_warn.records

    def test_step_calls_read_and_update(self):
        a = mock_application()

        with testfixtures.LogCapture(level=logging.WARNING) as l_warn:
            a._step(timestamp=1453928000)

        assert a._read_sources.call_count == 1
        assert a._sources[0].read.call_count == 1
        a._read_sources.assert_called_with(timestamp=1453928000)

        assert a._update_targets.call_count == 1
        assert a._targets[0].update.call_count == 1
        assert a._targets[1].update.call_count == 1
        a._update_targets.assert_called_with({'timestamp': 1453928000, 'value': 0.5})

        # Check that no events are logged
        assert not l_warn.records

    def test_step_skips_update_when_no_data(self):
        a = mock_application()
        a._sources[0].read.return_value = {}

        with testfixtures.LogCapture(level=logging.WARNING) as l_warn:
            a._step(timestamp=1453928000)

        assert a._read_sources.call_count == 1
        assert a._sources[0].read.call_count == 1
        a._read_sources.assert_called_with(timestamp=1453928000)

        assert a._update_targets.call_count == 0
        assert a._targets[0].update.call_count == 0
        assert a._targets[1].update.call_count == 0

        # Check that no events are logged
        assert not l_warn.records

    def test_step_skips_update_when_only_null_data(self):
        a = mock_application()
        a._sources[0].read.return_value = {'value': None}

        with testfixtures.LogCapture(level=logging.WARNING) as l_warn:
            a._step(timestamp=1453928000)

        assert a._read_sources.call_count == 1
        assert a._sources[0].read.call_count == 1
        a._read_sources.assert_called_with(timestamp=1453928000)

        assert a._update_targets.call_count == 0
        assert a._targets[0].update.call_count == 0
        assert a._targets[1].update.call_count == 0

        # Check that no events are logged
        assert not l_warn.records

    def test_target_exceptions_are_logged_and_continue(self):
        a = mock_application()

        t_fail = a._targets[0]
        t_fail.update.side_effect = ValueError('Invalid value')

        with testfixtures.LogCapture(level=logging.WARNING) as l:
            a._step(timestamp=1453928000)

        assert a._read_sources.call_count == 1
        assert a._sources[0].read.call_count == 1
        a._read_sources.assert_called_with(timestamp=1453928000)

        assert a._update_targets.call_count == 1
        assert a._targets[0].update.call_count == 1
        assert a._targets[1].update.call_count == 1
        a._update_targets.assert_called_with({'timestamp': 1453928000, 'value': 0.5})

        # Check that exception is logged
        assert len(l.records) == 1
        assert l.records[0].levelname == 'ERROR'
        assert (l.records[0].getMessage() ==
                "Failed to update DataTarget(name='Target 1') because of ValueError('Invalid value',)")

    def test_step_overrides_null_data(self):
        a = mock_application()
        a._sources[0].read.return_value = {'value': 0.5, 'timestamp': None}

        with testfixtures.LogCapture(level=logging.WARNING) as l:
            a._step(timestamp=1453928000)

        a._read_sources.assert_called_with(timestamp=1453928000)
        a._update_targets.assert_called_with({'timestamp': 1453928000, 'value': 0.5})
        assert not l.records

    def test_step_does_not_override_data(self):
        a = mock_application()
        a._sources[0].read.return_value = {'value': 0.5, 'timestamp': 14539230000}

        with testfixtures.LogCapture(level=logging.WARNING) as l:
            a._step(timestamp=1453928000)

        a._read_sources.assert_called_with(timestamp=1453928000)
        a._update_targets.assert_called_with({'timestamp': 14539230000, 'value': 0.5})
        assert not l.records

    def test_read_sources_calls_all_sources(self):
        a = mock_application()
        a.add_source(mock_source('Source 2', fieldX=2))

        with testfixtures.LogCapture(level=logging.WARNING) as l:
            data = a._read_sources(timestamp=1453928000)

        assert data == {'value': 0.5, 'fieldX': 2}
        assert not l.records

    def test_read_sources_throws_for_duplicate_fields(self):
        a = mock_application()
        a.add_source(mock_source('Source 2', value=2))

        with testfixtures.LogCapture(level=logging.WARNING) as l:
            with pytest.raises(DuplicateFieldError):
                _ = a._read_sources(timestamp=1453928000)

        assert len(l.records) == 1
        assert l.records[0].levelname == 'CRITICAL'
        assert (l.records[0].getMessage() ==
                "Duplicate data fields found: ['value']")

    def test_list_of_duplicate_fields_is_sorted_and_unique(self):
        a = mock_application()
        a.add_source(mock_source('Source 2', value=2, xyz=3, aaa=4))
        a.add_source(mock_source('Source 3', value=0, xyz=1, aaa=-1))

        with testfixtures.LogCapture(level=logging.WARNING) as l:
            with pytest.raises(DuplicateFieldError):
                _ = a._read_sources(timestamp=1453928000)

        assert len(l.records) == 1
        assert l.records[0].levelname == 'CRITICAL'
        assert (l.records[0].getMessage() ==
                "Duplicate data fields found: ['aaa', 'value', 'xyz']")


def mock_application():
    tf = mock.Mock()
    df = mock.Mock()

    a = Controller(timefcn=tf, delayfcn=df)

    s = mock_source('Source 1')
    a.add_source(s)

    for count in range(2):
        t = mock_target('Target {}'.format(count + 1))
        a.add_target(t)

    a._read_sources = mock.Mock(wraps=a._read_sources)
    a._update_targets = mock.Mock(wraps=a._update_targets)

    return a


def mock_source(name='', **kwargs):
    if not kwargs:
        kwargs = {'value': 0.5}

    obj = DataSource(name=name)
    obj.open = mock.Mock(wraps=obj.open)
    obj.close = mock.Mock(wraps=obj.close)
    obj.read = mock.Mock()
    obj.read.return_value = kwargs
    return obj


def mock_target(name=''):
    obj = DataTarget(name=name)
    obj.open = mock.Mock(wraps=obj.open)
    obj.close = mock.Mock(wraps=obj.close)
    obj.update = mock.Mock()
    return obj
