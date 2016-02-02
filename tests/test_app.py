import pytest
from unittest.mock import Mock

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
