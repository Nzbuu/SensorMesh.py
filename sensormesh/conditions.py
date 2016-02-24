class ConditionFactory:
    def __init__(self):
        super().__init__()
        self._map = {
            'delta_time_exceeds': DeltaTime
        }

    def prepare_conditions(self, conditions):
        if isinstance(conditions, dict):
            conditions = [self.create_condition(name, args)
                          for name, args in conditions.items()]
        return conditions

    def create_condition(self, name, args):
        cond_cls = self._map[name]

        if isinstance(args, (list, tuple)):
            return cond_cls(*args)
        else:
            return cond_cls(args)


class Condition:
    def check(self, **kwargs):
        raise NotImplementedError()

    def update(self, **kwargs):
        # Default is that there is no state
        pass

    def __str__(self):
        return '{0}()'.format(self.__class__.__name__)


class DeltaTime(Condition):
    def __init__(self, threshold):
        super().__init__()
        if threshold >= 0:
            self._time_step = threshold
        else:
            raise ValueError('Time step must be non-negative.')
        self._time_next = None

    @property
    def threshold(self):
        return self._time_step

    def check(self, timestamp, **kwargs):
        if self._time_next is None:
            # First call: always pass
            result = True
            self._time_next = timestamp
        else:
            # Take first time that exceeds next one
            result = timestamp >= self._time_next

        return result

    def update(self, timestamp, **kwargs):
        # Calculate time of next read/update
        super().update(**kwargs)
        self._time_next = timestamp + self._time_step

    def __str__(self):
        return '{0}(threshold={1})'.format(
            self.__class__.__name__, self._time_step)
