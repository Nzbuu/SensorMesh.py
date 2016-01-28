import time

from .exceptions import ConfigurationError


class App(object):
    def __init__(self):
        self.name = "SensorMesh"
        self._source = None
        self._loggers = []
        self._step = 20
        self._num_steps = 5

    def add_source(self, source):
        if self._source is None:
            self._source = source
        else:
            raise ConfigurationError()

    def add_logger(self, logger):
        self._loggers.append(logger)

    def _check_for_source(self):
        if self._source is None:
            raise ConfigurationError()

    def _check_for_loggers(self):
        if self._loggers is None:
            raise ConfigurationError()

    def start(self):
        self._check_for_source()
        self._check_for_loggers()

        time_start_next = time.time()
        for count_steps in range(self._num_steps):
            self.step()

            time_finish_now = time.time()
            time_start_next += self._step
            time.sleep(time_start_next - time_finish_now)

    def step(self):
        timestamp = time.time()

        data = self._source.read()
        if not data.get('timestamp', None):
            data['timestamp'] = timestamp

        for l in self._loggers:
            l.update(**data)
