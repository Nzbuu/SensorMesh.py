import unittest.mock as mock
import logging

import testfixtures

from sensormesh.endpoints import DataEndpoint, DataSource, DataTarget
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


class TestSource:
    def test_read_continues_when_checks_pass(self):
        s = mock_source(name='mock_source')

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            with s:
                result = s.read(timestamp=1)

        assert result == {'field1': 5, 'field2': -7}
        s._check_conditions.assert_called_once_with(timestamp=1)
        s._read.assert_called_once_with()
        s._update_conditions.assert_called_once_with(timestamp=1)

        assert len(l.records) == 3
        assert_record_is(l.records[0], 'INFO', "Opening DataSource(name='mock_source')")
        assert_record_is(l.records[1], 'INFO', "Reading DataSource(name='mock_source')")
        assert_record_is(l.records[2], 'INFO', "Closing DataSource(name='mock_source')")

    def test_read_stops_when_checks_fail(self):
        s = mock_source(name='mock_source')
        s._check_conditions = mock.Mock(return_value=(False, 'MyCondition(threshold=9)'))

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            with s:
                result = s.read(timestamp=1)

        assert result == {}
        s._check_conditions.assert_called_once_with(timestamp=1)
        assert s._read.call_count == 0
        assert s._update_conditions.call_count == 0

        assert len(l.records) == 3
        assert_record_is(l.records[0], 'INFO', "Opening DataSource(name='mock_source')")
        assert_record_is(l.records[1], 'INFO',
                         ("Skipping read of DataSource(name='mock_source') because "
                          "of MyCondition(threshold=9)"))
        assert_record_is(l.records[2], 'INFO', "Closing DataSource(name='mock_source')")


class TestTarget:
    def test_update_continues_when_checks_pass(self):
        t = mock_target(name='mock_target')

        data = {'timestamp': 2, 'field1': 5, 'field2': -7}

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            with t:
                t.update(data)

        t._check_conditions.assert_called_once_with(**data)
        t._update.assert_called_once_with(data)
        t._update_conditions.assert_called_once_with(**data)

        assert len(l.records) == 3
        assert_record_is(l.records[0], 'INFO', "Opening DataTarget(name='mock_target')")
        assert_record_is(l.records[1], 'INFO', "Updating DataTarget(name='mock_target')")
        assert_record_is(l.records[2], 'INFO', "Closing DataTarget(name='mock_target')")

    def test_update_stops_when_checks_fail(self):
        t = mock_target(name='mock_target')
        t._check_conditions = mock.Mock(return_value=(False, 'MyCondition(threshold=10)'))

        data = {'timestamp': 2, 'field1': 5, 'field2': -7}

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            with t:
                t.update(data)

        t._check_conditions.assert_called_once_with(**data)
        assert t._update.call_count == 0
        assert t._update_conditions.call_count == 0

        assert len(l.records) == 3
        assert_record_is(l.records[0], 'INFO', "Opening DataTarget(name='mock_target')")
        assert_record_is(l.records[1], 'INFO',
                         ("Skipping update of DataTarget(name='mock_target') because "
                          "of MyCondition(threshold=10)"))
        assert_record_is(l.records[2], 'INFO', "Closing DataTarget(name='mock_target')")

    def test_data_from_skipped_update_used_by_next(self):
        t = mock_target(name='mock_target')
        t._check_conditions = mock.Mock(side_effect=[
            (False, 'MyCondition(threshold=10)'),
            (True, None)
        ])

        data = [
            {'timestamp': 2, 'field1': 5, 'field2': -7},
            {'timestamp': 3, 'field1': 6}
            ]
        data_all = {
            'timestamp': 3, 'field1': 6, 'field2': -7
        }

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            with t:
                t.update(data[0])

                t._check_conditions.assert_called_once_with(**data[0])
                assert t._update.call_count == 0
                assert t._update_conditions.call_count == 0

                t.update(data[1])

                t._check_conditions.assert_called_with(**data_all)
                t._update.assert_called_with(data_all)
                t._update_conditions.assert_called_with(**data_all)

    def test_data_from_successful_update_is_not_in_next(self):
        t = mock_target(name='mock_target')
        t._check_conditions = mock.Mock(return_value=(True, None))

        data = [
            {'timestamp': 2, 'field1': 5, 'field2': -7},
            {'timestamp': 3, 'field1': 6}
            ]

        with testfixtures.LogCapture(level=logging.DEBUG) as l:
            with t:
                t.update(data[0])

                t._check_conditions.assert_called_with(**data[0])
                t._update.assert_called_with(data[0])
                t._update_conditions.assert_called_with(**data[0])

                t.update(data[1])

                t._check_conditions.assert_called_with(**data[1])
                t._update.assert_called_with(data[1])
                t._update_conditions.assert_called_with(**data[1])


def mock_source(**kwargs):
    obj = DataSource(**kwargs)
    obj._read = mock.Mock(return_value={'field1': 5, 'field2': -7})
    obj._check_conditions = mock.Mock(return_value=(True, None))
    obj._update_conditions = mock.Mock()
    return obj


def mock_target(**kwargs):
    obj = DataTarget(**kwargs)
    obj._update = mock.Mock()
    obj._check_conditions = mock.Mock(return_value=(True, None))
    obj._update_conditions = mock.Mock()
    return obj


def mock_condition(**kwargs):
    if not kwargs:
        kwargs['return_value'] = True
    str = kwargs.pop('str', 'Condition()')

    obj = mock.MagicMock(spec=Condition)
    obj.check = mock.MagicMock(**kwargs)
    obj.__str__.return_value = str

    return obj


def assert_record_is(record, level, message):
    assert record.levelname == level
    assert record.getMessage() == message
