import time

from .exceptions import ConfigurationError


class App(object):
    def __init__(self):
        self.name = "SensorMesh"
        self.__source = None
        self.__loggers = []
        self.__step = 20
        self.__num_steps = 5

    def add_source(self, source):
        if self.__source is None:
            self.__source = source
        else:
            raise ConfigurationError()

    def add_logger(self, logger):
        self.__loggers.append(logger)

    def _check_for_source(self):
        if self.__source is None:
            raise ConfigurationError()

    def _check_for_loggers(self):
        if self.__loggers is None:
            raise ConfigurationError()

    def start(self):
        self._check_for_source()
        self._check_for_loggers()

        time_start_next = time.time()
        for count_steps in range(self.__num_steps):
            self.step()

            time_finish_now = time.time()
            time_start_next += self.__step
            time.sleep(time_start_next - time_finish_now)

    def step(self):
        timestamp = time.time()

        data = self.__source.read()
        if not data.get('timestamp', None):
            data['timestamp'] = timestamp

        for l in self.__loggers:
            l.update(**data)
