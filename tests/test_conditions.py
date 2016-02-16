import pytest

from sensormesh.conditions import *


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

    def test_passes_first_step(self):
        obj = TimeCheck(time_step=1)
        result = obj.check(timestamp=0)
        assert result

    def test_passes_second_step_with_zero_step(self):
        obj = TimeCheck(time_step=0)
        _ = obj.check(timestamp=0)
        result = obj.check(timestamp=0)
        assert result

    def test_fails_second_step_with_small_step(self):
        obj = TimeCheck(time_step=1)
        _ = obj.check(timestamp=0)
        result = obj.check(timestamp=0.1)
        assert not result

    def test_fails_until_time_elapsed(self):
        obj = TimeCheck(time_step=5)
        t = 0
        _ = obj.check(timestamp=t)
        while not obj.check(timestamp=t):
            t += 2
        assert t == 6

    def test_to_str(self):
        obj = TimeCheck(time_step=5)
        assert str(obj) == 'TimeCheck(time_step=5)'
