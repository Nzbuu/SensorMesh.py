import os.path
import time
import json
import contextlib

from .exceptions import ConfigurationError


class Controller(object):
    def __init__(self, name="SensorMesh", timefcn=None, delayfcn=None):
        self.name = name
        self._source = None
        self._targets = []
        self._time_step = 0
        self._num_steps = 1

        self._timefcn = timefcn if timefcn else time.time
        self._delayfcn = delayfcn if delayfcn else time.sleep

    def set_steps(self, step, num_steps):
        self._time_step = step
        self._num_steps = num_steps

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
        if not self._source:
            raise ConfigurationError()

    def _check_for_targets(self):
        if not self._targets:
            raise ConfigurationError()

    def run(self):
        self._check_for_source()
        self._check_for_targets()

        with contextlib.ExitStack() as stack:
            self._start(stack)

            time_start_next = self._timefcn()
            for count_steps in range(self._num_steps):
                self._step()

                if self._time_step <= 0:
                    pass
                elif count_steps < self._num_steps - 1:
                    time_finish_now = self._timefcn()
                    time_start_next += self._time_step
                    while time_finish_now > time_start_next:
                        time_start_next += self._time_step

                    self._delayfcn(max(time_start_next - time_finish_now, 0))

    def _start(self, stack=None):
        s = self._source
        s.open()
        if stack:
            stack.callback(s.close)

        for t in self._targets:
            t.open()
            if stack:
                stack.callback(t.close)

    def _step(self):
        timestamp = self._timefcn()

        data = self._source.read()
        if not data.get('timestamp'):
            data['timestamp'] = timestamp

        for t in self._targets:
            t.update(data)


class ConfigManager(object):
    def __init__(self):
        self._map = {
            '.json': self.load_json_file,
        }

    def load_config_file(self, filename):
        _, fileext = os.path.splitext(filename)
        load_fcn = self._map[fileext]
        return load_fcn(filename)

    def load_json_file(self, filename):
        with open(filename) as cfg_file:
            cfg_data = json.load(cfg_file)
        return cfg_data
