import os.path
import time
import json
import contextlib
import logging

from .exceptions import ConfigurationError, DuplicateFieldError

logger = logging.getLogger(__name__)


class Controller(object):
    def __init__(self, name="SensorMesh", timefcn=None, delayfcn=None):
        self.name = name
        self._sources = []
        self._targets = []

        self._trigger = TimeTrigger(timefcn, delayfcn)

    def set_steps(self, time_step, num_steps):
        self._trigger.set_steps(time_step, num_steps)

    def add_source(self, source):
        self._sources.append(source)

    def add_target(self, target):
        self._targets.append(target)

    def get_source_names(self):
        return tuple(s.name for s in self._sources)

    def get_target_names(self):
        return tuple(t.name for t in self._targets)

    def _check_for_sources(self):
        if not self._sources:
            raise ConfigurationError('Source object is missing')

    def _check_for_targets(self):
        if not self._targets:
            raise ConfigurationError('Target object is missing')

    def run(self):
        logger.info('Starting Controller')

        self._check_for_sources()
        self._check_for_targets()

        with contextlib.ExitStack() as stack:
            self._start(stack)

            for timestamp in self._trigger.iter():
                self._step(timestamp=timestamp)

    def _start(self, stack):
        for o in self._sources:
            stack.enter_context(o)
        for o in self._targets:
            stack.enter_context(o)

    def _step(self, **kwargs):
        data = self._read_sources(**kwargs)

        if all(v is None for v in data.values()):
            logger.info('Read data is empty')
            return

        for k in kwargs:
            if data.get(k) is not None:
                data[k] = kwargs[k]

        self._update_targets(data)

    def _read_sources(self, **kwargs):
        data = {}
        duplicate_fields = set()
        for s in self._sources:
            s_data = s.read(**kwargs)
            duplicate_fields.update(data.keys() & s_data.keys())
            data.update(**s_data)

        if duplicate_fields:
            duplicate_fields = sorted(duplicate_fields)
            str = 'Duplicate data fields found: {0!s}'.format(duplicate_fields)
            logger.critical(str)
            raise DuplicateFieldError(str)

        return data

    def _update_targets(self, data):
        for t in self._targets:
            try:
                t.update(data)
            except Exception as e:
                # Log exception as error, rather than exception for simpler
                # log message. Continue afterwards.
                logger.error('Failed to update %s: %r', t, e)


class TimeTrigger(object):
    def __init__(self, timefcn, delayfcn):
        self._timefcn = timefcn if timefcn else time.time
        self._delayfcn = delayfcn if delayfcn else time.sleep
        self._num_steps = 1
        self._time_step = 0

    def set_steps(self, time_step, num_steps):
        self._time_step = time_step
        self._num_steps = num_steps

    def iter(self):
        logger.info('Starting iterator')

        time_finish_now = self._timefcn()
        time_start_next = time_finish_now

        for count_steps in range(self._num_steps):
            if time_start_next > time_finish_now:
                self._delayfcn(time_start_next - time_finish_now)

            logger.info('Start iteration #%d', count_steps)
            yield time_start_next

            time_finish_now = self._timefcn()
            if self._time_step > 0:
                time_start_next += self._time_step
                while time_finish_now > time_start_next:
                    time_start_next += self._time_step
            else:
                time_start_next = time_finish_now

        logger.info('Finished iterator')


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
