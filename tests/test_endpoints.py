import pytest

from sensormesh.endpoints import DataEndpoint as BaseClass


class TestBase:
    def test_can_create_base_class(self):
        o = BaseClass()
        assert o.name == ''
        assert o._adapter.count == 0

    def test_can_set_name(self):
        o = BaseClass(name='Name')
        assert o.name == 'Name'
        assert o._adapter.count == 0

    def test_can_configure_direct_fields(self):
        o = BaseClass(fields=['val2', 'val1', 'val3'])
        assert o._adapter.count == 3
        assert o.fields == ['val2', 'val1', 'val3']
        assert o._adapter._local_to_remote == {'val1': 'val1', 'val2': 'val2', 'val3': 'val3'}

    def test_can_configure_indirect_fields(self):
        o = BaseClass(fields=[('l', 'r')])
        assert o._adapter.count == 1
        assert o.fields == ['l']
        assert o._adapter._local_to_remote == {'l': 'r'}
