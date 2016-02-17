import unittest.mock as mock

from sensormesh.endpoints import DataEndpoint
from sensormesh.conditions import Condition


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
        mock_cond = mock_condition()
        o = DataEndpoint()
        o.add_condition(mock_cond)
        assert o._conditions == [mock_cond]

    def test_can_add_multiple_conditions_in_order(self):
        mock_cond1 = mock_condition()
        mock_cond2 = mock_condition()
        o = DataEndpoint()
        o.add_condition(mock_cond1)
        o.add_condition(mock_cond2)
        assert o._conditions == [mock_cond1, mock_cond2]

    def test_all_conditions_checked(self):
        c1 = mock_condition(str='Condition(1)')
        c2 = mock_condition(str='Condition(2)')
        o = DataEndpoint()
        o.add_condition(c1)
        o.add_condition(c2)

        result, reason = o._check_conditions(value=1)

        assert result
        assert not reason

        c1.check.assert_called_once_with(value=1)
        c2.check.assert_called_once_with(value=1)
        assert not c1.update.called
        assert not c2.update.called

    def test_checks_returns_false_and_reason_when_one_fails(self):
        c1 = mock_condition(str='Condition(1)')
        c2 = mock_condition(return_value=False, str='Condition(2)')
        o = DataEndpoint()
        o.add_condition(c1)
        o.add_condition(c2)

        result, reason = o._check_conditions(value=2)

        assert not result
        assert reason == 'Condition(2)'

        c1.check.assert_called_once_with(value=2)
        c2.check.assert_called_once_with(value=2)
        assert not c1.update.called
        assert not c2.update.called

    def test_shortcut_checks_when_one_fails(self):
        c1 = mock_condition(return_value=False, str='Condition(1)')
        c2 = mock_condition(str='Condition(2)')
        o = DataEndpoint()
        o.add_condition(c1)
        o.add_condition(c2)

        result, reason = o._check_conditions(value=3)

        assert not result
        assert reason == 'Condition(1)'

        c1.check.assert_called_once_with(value=3)
        assert c2.check.call_count == 0
        assert not c1.update.called
        assert not c2.update.called

    def test_all_conditions_are_updated_regardless_of_result(self):
        c1 = mock_condition(return_value=False, str='Condition(1)')
        c2 = mock_condition(str='Condition(2)')
        o = DataEndpoint()
        o.add_condition(c1)
        o.add_condition(c2)

        o._update_conditions(value=4)

        assert not c1.check.called
        assert not c2.check.called
        c1.update.assert_called_once_with(value=4)
        c2.update.assert_called_once_with(value=4)


def mock_condition(**kwargs):
    if not kwargs:
        kwargs['return_value'] = True
    str = kwargs.pop('str', 'Condition()')

    cond = mock.MagicMock(spec=Condition)
    cond.check = mock.MagicMock(**kwargs)
    cond.__str__.return_value = str

    return cond
