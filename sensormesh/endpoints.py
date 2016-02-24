import logging

from .utils import DataAdapter
from .conditions import ConditionFactory

logger = logging.getLogger(__name__)


class DataEndpoint(object):
    def __init__(self, name='', fields=(), when=(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._conditions = []
        self._adapter = DataAdapter()

        if isinstance(when, dict):
            cond_fact = ConditionFactory()
            when = cond_fact.prepare_conditions(when)
        for condition in when:
            self.add_condition(condition)

        for name in fields:
            if isinstance(name, str):
                self._add_field(name)
            else:
                self._add_field(*name)

    @property
    def name(self):
        return self._name

    @property
    def fields(self):
        return list(self._adapter.local_names)

    @property
    def fields_remote(self):
        return list(self._adapter.remote_names)

    def _add_field(self, local_name, remote_name=None):
        if not remote_name:
            remote_name = local_name

        self._adapter.add_field(
            local_name=local_name,
            remote_name=remote_name
        )

    def add_condition(self, condition):
        self._conditions.append(condition)

    def _check_conditions(self, **kwargs):
        for cond in self._conditions:
            if not cond.check(**kwargs):
                return False, str(cond)
        return True, None

    def _update_conditions(self, **kwargs):
        for cond in self._conditions:
            cond.update(**kwargs)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        logger.info('Opening %s', self)

    def close(self):
        logger.info('Closing %s', self)

    def __str__(self):
        return "{0}(name={1!r})".format(self.__class__.__name__, self._name)


class DataSource(DataEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self, **kwargs):
        # Check whether to continue with read
        result, reason = self._check_conditions(**kwargs)
        if result:
            logger.info('Reading %s', self)

            # Do read
            data_in = self._read()

            # Process data packet from read
            data = self._process_data(data_in)

            # Record successful read
            self._update_conditions(**kwargs)
        else:
            # Log skipped read
            logger.info('Skipping read of %s because of %s', self, reason)

            # Return empty data packet
            data = {}

        return data

    def _read(self):
        raise NotImplementedError()

    def _process_data(self, data):
        if self._adapter.count:
            return self._adapter.create_local_struct(data)
        else:
            return data


class DataTarget(DataEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cache of unused data
        self._data = {}

    def update(self, data):
        # Update cache of unused data
        self._data.update(data)

        # Check whether to continue with update
        result, reason = self._check_conditions(**self._data)
        if result:
            logger.info('Updating %s', self)

            # Prepare data packet for update
            data_out = self._prepare_update(self._data)

            # Do update
            self._update(data_out)

            # Record successful update
            self._update_conditions(**self._data)

            # Clear cache of unused data
            self._data = {}
        else:
            # Log skipped update
            logger.info('Skipping update of %s because of %s', self, reason)

    def _prepare_update(self, data):
        if self._adapter.count:
            return self._adapter.create_remote_struct(data)
        else:
            return data

    def _update(self, data):
        raise NotImplementedError()
