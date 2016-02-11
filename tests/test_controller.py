import unittest.mock as mock

import pytest

from sensormesh.application import *
from sensormesh.base import DataSource, DataTarget


class TestController:
    def test_can_create_app(self):
        a = Controller()

    def test_can_add_source(self):
        a = Controller()
        s = DataSource()
        s.name = 'Mock Source'
        a.add_source(s)
        assert a.get_source_name() == 'Mock Source'

    def test_cannot_add_2_sources(self):
        a = Controller()
        s1 = DataSource()
        s2 = DataSource()
        a.add_source(s1)
        with pytest.raises(ConfigurationError):
            a.add_source(s2)

    def test_can_add_target(self):
        a = Controller()
        t = DataTarget()
        t.name = 'Mock Target'
        a.add_target(t)
        assert a.get_target_names() == ['Mock Target']

    def test_can_add_2_targets(self):
        a = Controller()
        t1 = DataTarget()
        t1.name = 'Mock Target 1'
        t2 = DataTarget()
        t2.name = 'Mock Target 2'
        a.add_target(t1)
        a.add_target(t2)
        assert a.get_target_names() == ['Mock Target 1', 'Mock Target 2']

    def test_cannot_start_without_target(self):
        a = Controller()
        s = DataSource()
        a.add_source(s)
        with pytest.raises(ConfigurationError):
            a.run()

    def test_cannot_start_without_source(self):
        a = Controller()
        t = DataTarget()
        a.add_target(t)
        with pytest.raises(ConfigurationError):
            a.run()

    def test_runs_with_zero_step(self):
        a = mock_application()
        a._timefcn.side_effect = [1453928000, 1453928000.1, 1453928000.2]
        a.set_steps(step=0, num_steps=2)
        a._step = mock.Mock()

        a.run()

        assert a._step.call_count == 2
        assert a._delayfcn.call_count == 0  # Never sleeps

        # All resources started
        assert a._source.open.call_count == 1
        assert a._targets[0].open.call_count == 1
        assert a._targets[1].open.call_count == 1

        # All resources stopped
        assert a._source.close.call_count == 1
        assert a._targets[0].close.call_count == 1
        assert a._targets[1].close.call_count == 1

    def test_runs_with_nonzero_step(self):
        a = mock_application()
        a._timefcn.side_effect = [1453928000, 1453928000.1, 1453928001.1]
        a.set_steps(step=1, num_steps=2)
        a._step = mock.Mock()

        a.run()

        assert a._step.call_count == 2
        assert a._delayfcn.call_count == 1  # Don't delay after final step

        # All resources started
        assert a._source.open.call_count == 1
        assert a._targets[0].open.call_count == 1
        assert a._targets[1].open.call_count == 1

        # All resources stopped
        assert a._source.close.call_count == 1
        assert a._targets[0].close.call_count == 1
        assert a._targets[1].close.call_count == 1

    def test_skips_missing_steps(self):
        a = mock_application()
        a._timefcn.side_effect = [1453928000, 1453928001.1, 1453928003.1]
        a.set_steps(step=1, num_steps=2)
        a._step = mock.Mock()

        a.run()

        assert a._step.call_count == 2
        assert a._delayfcn.call_count == 1  # Don't delay after final step

        # All resources started
        assert a._source.open.call_count == 1
        assert a._targets[0].open.call_count == 1
        assert a._targets[1].open.call_count == 1

        # All resources stopped
        assert a._source.close.call_count == 1
        assert a._targets[0].close.call_count == 1
        assert a._targets[1].close.call_count == 1

    def test_step_calls_read_and_update(self):
        a = mock_application()
        a._timefcn.side_effect = [1453928000, 1453928000.1, 1453928001.1]

        a._step()

        assert a._source.read.call_count == 1
        assert a._targets[0].update.call_count == 1
        assert a._targets[1].update.call_count == 1


def mock_application():
    tf = mock.Mock()
    df = mock.Mock()

    a = Controller(timefcn=tf, delayfcn=df)

    s = mock_source()
    a.add_source(s)

    for _ in range(2):
        t = mock_target()
        a.add_target(t)

    return a


def mock_source(name=''):
    s = DataSource(name=name)
    s.open = mock.Mock()
    s.close = mock.Mock()
    s.read = mock.Mock()
    s.read.return_value = {'value': 0.5}
    return s


def mock_target(name=''):
    t = DataTarget(name=name)
    t.open = mock.Mock()
    t.close = mock.Mock()
    t.update = mock.Mock()
    return t
