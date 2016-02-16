import unittest.mock as mock

from sensormesh.endpoints import DataEndpoint


class TestBase:
    def test_can_create_base_class(self):
        o = DataEndpoint()
        assert o.name == ''
        assert o._adapter.count == 0

    def test_can_set_name(self):
        o = DataEndpoint(name='Name')
        assert o.name == 'Name'
        assert o._adapter.count == 0

    def test_can_configure_direct_fields(self):
        o = DataEndpoint(fields=['val2', 'val1', 'val3'])
        assert o._adapter.count == 3
        assert o.fields == ['val2', 'val1', 'val3']
        assert o._adapter._local_to_remote == {'val1': 'val1', 'val2': 'val2', 'val3': 'val3'}

    def test_can_configure_indirect_fields(self):
        o = DataEndpoint(fields=[('l', 'r')])
        assert o._adapter.count == 1
        assert o.fields == ['l']
        assert o._adapter._local_to_remote == {'l': 'r'}

    def test_can_configure_conditions(self):
        mock_cond = mock.MagicMock()
        o = DataEndpoint(when=[mock_cond])
        assert o._conditions == [mock_cond]

    def test_can_add_conditions(self):
        mock_cond = mock.MagicMock()
        o = DataEndpoint()
        o.add_condition(mock_cond)
        assert o._conditions == [mock_cond]

    def test_can_add_multiple_conditions_in_order(self):
        mock_cond1 = mock.MagicMock()
        mock_cond2 = mock.MagicMock()
        o = DataEndpoint()
        o.add_condition(mock_cond1)
        o.add_condition(mock_cond2)
        assert o._conditions == [mock_cond1, mock_cond2]
