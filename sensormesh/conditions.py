class Condition:
    def check(self, **kwargs):
        raise NotImplementedError()


class TimeCheck(Condition):
    def __init__(self, time_min):
        super().__init__()
        self._time_step = time_min
        self._time_next = None

    def check(self, timestamp, **kwargs):
        if self._time_next is None:
            result = True
            self._time_next = timestamp
        else:
            result = timestamp >= self._time_next

        if result:
            self._time_next = timestamp + self._time_step
        return result

    def __str__(self):
        return '{0}(time_min={1})'.format(
            self.__class__.__name__, self._time_step)
