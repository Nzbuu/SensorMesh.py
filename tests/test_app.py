from unittest.mock import Mock

import pytest

from sensormesh.applications import *
from sensormesh.base import DataSource, DataTarget


class TestApp:
    def test_can_create_app(self):
        a = App()

    def test_can_add_source(self):
        a = App()
        s = DataSource()
        s.name = 'Mock Source'
        a.add_source(s)
        assert a.get_source_name() == 'Mock Source'

    def test_cannot_add_2_sources(self):
        a = App()
        s1 = DataSource()
        s2 = DataSource()
        a.add_source(s1)
        with pytest.raises(ConfigurationError):
            a.add_source(s2)

    def test_can_add_target(self):
        a = App()
        t = DataTarget()
        t.name = 'Mock Target'
        a.add_target(t)
        assert a.get_target_names() == ['Mock Target']

    def test_can_add_2_targets(self):
        a = App()
        t1 = DataTarget()
        t1.name = 'Mock Target 1'
        t2 = DataTarget()
        t2.name = 'Mock Target 2'
        a.add_target(t1)
        a.add_target(t2)
        assert a.get_target_names() == ['Mock Target 1', 'Mock Target 2']

    def test_cannot_start_without_target(self):
        a = App()
        s = DataSource()
        a.add_source(s)
        with pytest.raises(ConfigurationError):
            a.start()

    def test_cannot_start_without_source(self):
        a = App()
        t = DataTarget()
        a.add_target(t)
        with pytest.raises(ConfigurationError):
            a.start()

    def test_runs_with_zero_step(self):
        tf = Mock()
        tf.side_effect = [1453928000, 1453928000.1, 1453928000.2]
        df = Mock()

        a = App(timefcn=tf, delayfcn=df)
        a.set_steps(step=0, num_steps=2)
        a.step = Mock()

        s = DataSource()
        a.add_source(s)

        t = DataTarget()
        a.add_target(t)

        a.start()

        assert a.step.call_count == 2
        assert df.call_count == 0  # No delays when zero step

    def test_runs_with_nonzero_step(self):
        tf = Mock()
        tf.side_effect = [1453928000, 1453928000.1, 1453928001.1]
        df = Mock()

        a = App(timefcn=tf, delayfcn=df)
        a.set_steps(step=1, num_steps=2)
        a.step = Mock()

        s = DataSource()
        a.add_source(s)

        t = DataTarget()
        a.add_target(t)

        a.start()

        assert a.step.call_count == 2
        assert df.call_count == 1  # Don't delay after final step

    def test_skips_missing_steps(self):
        tf = Mock()
        tf.side_effect = [1453928000, 1453928001.1, 1453928003.1]
        df = Mock()

        a = App(timefcn=tf, delayfcn=df)
        a.set_steps(step=1, num_steps=2)
        a.step = Mock()

        s = DataSource()
        a.add_source(s)

        t = DataTarget()
        a.add_target(t)

        a.start()

        assert a.step.call_count == 2
        assert df.call_count == 1  # Don't delay after final step

    def test_step_calls_read_and_update(self):
        tf = Mock()
        tf.side_effect = [1453928000, 1453928000.1, 1453928001.1]
        df = Mock()

        a = App(timefcn=tf, delayfcn=df)

        s = DataSource()
        s.read = Mock()
        s.read.return_value = {'value': 0.5}
        a.add_source(s)

        t = DataTarget()
        t.update = Mock()
        a.add_target(t)

        a.step()

        assert s.read.call_count == 1
        assert t.update.call_count == 1

