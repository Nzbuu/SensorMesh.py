import time
import logging

logger = logging.getLogger(__name__)


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
