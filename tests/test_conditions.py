import unittest.mock as mock

import pytest

from sensormesh.conditions import Condition, ConditionFactory, DeltaTime


class TestCondition:
    def test_has_default_str_method(self):
        class MyCondition(Condition):
            pass

        o = MyCondition()
        assert str(o) == 'MyCondition()'


class TestConditionFactory:
    def test_create_condition_with_no_arguments(self):
        fact = mock_factory()
        cond = fact.create_condition('type_1', [])
        assert cond == mock.sentinel.type_1
        fact._map['type_1'].assert_called_with()
        assert not fact._map['type_2'].called

    def test_create_condition_with_one_argument(self):
        fact = mock_factory()
        cond = fact.create_condition('type_1', 5)
        assert cond == mock.sentinel.type_1
        fact._map['type_1'].assert_called_with(5)
        assert not fact._map['type_2'].called

    def test_create_condition_with_multiple_argument(self):
        fact = mock_factory()
        cond = fact.create_condition('type_2', [1, 2, 'jack'])
        assert cond == mock.sentinel.type_2
        fact._map['type_2'].assert_called_with(1, 2, 'jack')
        assert not fact._map['type_1'].called


def mock_factory():
    obj = ConditionFactory()
    obj._map = {
        'type_1': mock.MagicMock(return_value=mock.sentinel.type_1),
        'type_2': mock.MagicMock(return_value=mock.sentinel.type_2),
    }
    return obj


class TestDeltaTimeCond:
    def test_requires_time_step_argument(self):
        with pytest.raises(TypeError):
            _ = DeltaTime()

    def test_accepts_zero_time_step(self):
        obj = DeltaTime(0)
        assert obj.threshold == 0

    def test_accepts_positive_time_step(self):
        obj = DeltaTime(10)
        assert obj.threshold == 10

    def test_requires_nonnegative_time_step(self):
        with pytest.raises(ValueError):
            _ = DeltaTime(-1)

    def test_passes_first_step_always(self):
        obj = DeltaTime(threshold=1)
        result = obj.check(timestamp=0)
        assert result

    def test_passes_next_step_with_zero_step(self):
        obj = DeltaTime(threshold=0)
        obj.update(timestamp=0)  # record pass at time 0
        result = obj.check(timestamp=0)  # next step
        assert result

    def test_fails_next_step_with_small_step(self):
        obj = DeltaTime(threshold=1)
        obj.update(timestamp=0)  # record pass at time 0
        result = obj.check(timestamp=0.1)  # next step
        assert not result

    def test_passes_next_step_without_update(self):
        obj = DeltaTime(threshold=1)
        result_first = obj.check(timestamp=0)  # first step
        assert result_first
        result_next = obj.check(timestamp=0.1)  # next step
        assert result_next

    def test_fails_until_time_elapsed(self):
        obj = DeltaTime(threshold=5)
        t = 0
        obj.update(timestamp=t)  # record pass at time t
        while not obj.check(timestamp=t):  # next steps
            t += 2
        assert t == 6

    def test_to_str(self):
        obj = DeltaTime(threshold=5)
        assert str(obj) == 'DeltaTime(threshold=5)'
