class Condition:
    def check(self, **kwargs):
        raise NotImplementedError()


class TimeCheck(Condition):
    def __init__(self, time_step):
        super().__init__()
        if time_step >= 0:
            self._time_step = time_step
        else:
            raise ValueError('Time step must be non-negative.')
        self._time_next = None

    def check(self, timestamp, **kwargs):
        if self._time_next is None:
            # First call: always pass
            result = True
            self._time_next = timestamp
        else:
            # Take first time that exceeds next one
            result = timestamp >= self._time_next

        if result:
            # Calculate time of next read/update
            self._time_next = timestamp + self._time_step

        return result

    def __str__(self):
        return '{0}(time_step={1})'.format(
            self.__class__.__name__, self._time_step)
