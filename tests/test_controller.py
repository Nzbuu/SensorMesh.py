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
        tf = mock.Mock()
        tf.side_effect = [1453928000, 1453928000.1, 1453928000.2]
        df = mock.Mock()

        a = Controller(timefcn=tf, delayfcn=df)
        a.set_steps(step=0, num_steps=2)
        a._start = mock.Mock()
        a._step = mock.Mock()
        a._stop = mock.Mock()

        s = DataSource()
        a.add_source(s)

        t = DataTarget()
        a.add_target(t)

        a.run()

        assert a._start.call_count == 1
        assert a._step.call_count == 2
        assert a._stop.call_count == 1
        assert df.call_count == 0  # No delays when zero step

    def test_runs_with_nonzero_step(self):
        tf = mock.Mock()
        tf.side_effect = [1453928000, 1453928000.1, 1453928001.1]
        df = mock.Mock()

        a = Controller(timefcn=tf, delayfcn=df)
        a.set_steps(step=1, num_steps=2)
        a._start = mock.Mock()
        a._step = mock.Mock()
        a._stop = mock.Mock()

        s = DataSource()
        a.add_source(s)

        t = DataTarget()
        a.add_target(t)

        a.run()

        assert a._start.call_count == 1
        assert a._step.call_count == 2
        assert a._stop.call_count == 1
        assert df.call_count == 1  # Don't delay after final step

    def test_skips_missing_steps(self):
        tf = mock.Mock()
        tf.side_effect = [1453928000, 1453928001.1, 1453928003.1]
        df = mock.Mock()

        a = Controller(timefcn=tf, delayfcn=df)
        a.set_steps(step=1, num_steps=2)
        a._start = mock.Mock()
        a._step = mock.Mock()
        a._stop = mock.Mock()

        s = DataSource()
        a.add_source(s)

        t = DataTarget()
        a.add_target(t)

        a.run()

        assert a._start.call_count == 1
        assert a._step.call_count == 2
        assert a._stop.call_count == 1
        assert df.call_count == 1  # Don't delay after final step

    def test_step_calls_read_and_update(self):
        tf = mock.Mock()
        tf.side_effect = [1453928000, 1453928000.1, 1453928001.1]
        df = mock.Mock()

        a = Controller(timefcn=tf, delayfcn=df)

        s = DataSource()
        s.read = mock.Mock()
        s.read.return_value = {'value': 0.5}
        a.add_source(s)

        t = DataTarget()
        t.update = mock.Mock()
        a.add_target(t)

        a._step()

        assert s.read.call_count == 1
        assert t.update.call_count == 1
