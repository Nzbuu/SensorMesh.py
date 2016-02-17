import pytest

from sensormesh.conditions import *


class TestCondition:
    def test_has_default_str_method(self):
        class MyCondition(Condition):
            pass
        
        o = MyCondition()
        assert str(o) == 'MyCondition()'


class TestTimeCheck:
    def test_requires_time_step_argument(self):
        with pytest.raises(TypeError):
            _ = TimeCheck()

    def test_accepts_zero_time_step(self):
        obj = TimeCheck(0)
        assert obj._time_step == 0

    def test_accepts_positive_time_step(self):
        obj = TimeCheck(10)
        assert obj._time_step == 10

    def test_requires_nonnegative_time_step(self):
        with pytest.raises(ValueError):
            _ = TimeCheck(-1)

    def test_passes_first_step_always(self):
        obj = TimeCheck(time_step=1)
        result = obj.check(timestamp=0)
        assert result

    def test_passes_next_step_with_zero_step(self):
        obj = TimeCheck(time_step=0)
        obj.update(timestamp=0)  # record pass at time 0
        result = obj.check(timestamp=0)  # next step
        assert result

    def test_fails_next_step_with_small_step(self):
        obj = TimeCheck(time_step=1)
        obj.update(timestamp=0)  # record pass at time 0
        result = obj.check(timestamp=0.1)  # next step
        assert not result

    def test_passes_next_step_without_update(self):
        obj = TimeCheck(time_step=1)
        result_first = obj.check(timestamp=0)  # first step
        assert result_first
        result_next = obj.check(timestamp=0.1)  # next step
        assert result_next

    def test_fails_until_time_elapsed(self):
        obj = TimeCheck(time_step=5)
        t = 0
        obj.update(timestamp=t)  # record pass at time t
        while not obj.check(timestamp=t):  # next steps
            t += 2
        assert t == 6

    def test_to_str(self):
        obj = TimeCheck(time_step=5)
        assert str(obj) == 'TimeCheck(time_step=5)'
