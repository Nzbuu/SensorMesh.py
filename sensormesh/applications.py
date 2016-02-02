import time

from .exceptions import ConfigurationError


class App(object):
    def __init__(self, name="SensorMesh", timefcn=None, delayfcn=None):
        self.name = name
        self._source = None
        self._targets = []
        self._step = 20
        self._num_steps = 5

        self._timefcn = timefcn if timefcn else time.time
        self._delayfcn = delayfcn if delayfcn else time.sleep

    def add_source(self, source):
        if self._source is None:
            self._source = source
        else:
            raise ConfigurationError()

    def add_target(self, logger):
        self._targets.append(logger)

    def get_source_name(self):
        return self._source.name if self._source else None

    def get_target_names(self):
        return [t.name for t in self._targets]

    def _check_for_source(self):
        if self._source is None:
            raise ConfigurationError()

    def _check_for_targets(self):
        if self._targets is None:
            raise ConfigurationError()

    def start(self):
        self._check_for_source()
        self._check_for_targets()

        time_start_prev = self._timefcn()
        time_start_next = self._timefcn()
        for count_steps in range(self._num_steps):
            time_start_now = self._timefcn()
            print('step =', '{:f}'.format(time_start_now - time_start_prev))
            print('accuracy =', '{:f}'.format(time_start_now - time_start_next))
            time_start_prev = time_start_now

            self.step()

            if count_steps < self._num_steps - 1:
                time_finish_now = self._timefcn()
                time_start_next += self._step
                while time_finish_now > time_start_next:
                    time_start_next += self._step

                time_finish_now = self._timefcn()
                self._delayfcn(time_start_next - time_finish_now)

    def step(self):
        timestamp = self._timefcn()

        data = self._source.read()
        if not data.get('timestamp', None):
            data['timestamp'] = timestamp

        for l in self._targets:
            l.update(data)
