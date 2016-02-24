import pytest

from sensormesh.conditions import Condition, DeltaTime


class TestCondition:
    def test_has_default_str_method(self):
        class MyCondition(Condition):
            pass

        o = MyCondition()
        assert str(o) == 'MyCondition()'


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
