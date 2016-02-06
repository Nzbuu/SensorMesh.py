import pytest

from sensormesh.base import Base as BaseClass


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

    def test_can_configure_feeds(self):
        o = BaseClass(feeds={'field1': 'val1', 'field2': 'val2'})
        assert o._adapter.count == 2
        assert sorted(o.fields) == ['val1', 'val2']  # No guarantee that these will be in the specified order
        assert o._adapter._local_to_remote == {'val1': 'field1', 'val2': 'field2'}

    def test_cannot_use_both_feeds_and_fields(self):
        with pytest.raises(TypeError):
            _ = BaseClass(feeds={'field0': 'value'}, fields=[('value', 'field0')])
