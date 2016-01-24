import time

from .exceptions import ConfigurationError


class App(object):
    def __init__(self):
        self.name = "SensorMesh"
        self.__sensor = None
        self.__loggers = []
        self.__step = 20
        self.__num_steps = 5

    def add_sensor(self, s):
        if self.__sensor is None:
            self.__sensor = s
        else:
            raise ConfigurationError()

    def _check_for_sensor(self):
        if self.__sensor is None:
            raise ConfigurationError()

    def _check_for_loggers(self):
        if self.__sensor is None:
            raise ConfigurationError()

    def add_logger(self, l):
        self.__loggers.append(l)

    def start(self):
        self._check_for_sensor()
        self._check_for_loggers()

        time_start_next = time.time()
        for count_steps in range(self.__num_steps):
            self.step()

            time_finish_now = time.time()
            time_start_next += self.__step
            time.sleep(time_start_next - time_finish_now)

    def step(self):
        time_stamp = time.time()

        measurement = self.__sensor.read()
        if measurement.get('time', None) is None:
            measurement['time'] = time_stamp

        for l in self.__loggers:
            l.add(**measurement)
