import logging

from .utils import DataAdapter

logger = logging.getLogger(__name__)


class DataEndpoint(object):
    def __init__(self, name='', fields=(), when=()):
        super().__init__()
        self._name = name
        self._adapter = DataAdapter()

        self._condition = []
        for w in when:
            self._add_condition(w)

        for name in fields:
            if isinstance(name, str):
                self._add_field(name)
            else:
                self._add_field(
                    local_name=name[0],
                    remote_name=name[1])

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

    def _add_condition(self, condition):
        pass

    def _check_conditions(self, **kwargs):
        return True

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        logger.info('Opening %s', str(self))

    def close(self):
        logger.info('Closing %s', str(self))

    def __str__(self):
        return "{0}(name='{1}')".format(self.__class__.__name__, self._name)


class DataSource(DataEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self, **kwargs):
        if self._check_conditions(**kwargs):
            logger.info('Read %s', str(self))
            data_in = self._read()
            data = self._process_data(data_in)
            return data
        else:
            logger.info('Skip read %s', str(self))
            return {}

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

    def update(self, data):
        if self._check_conditions(**data):
            logger.info('Update %s', str(self))
            data_out = self._prepare_update(data)
            self._update(data_out)
        else:
            logger.info('Skip update %s', str(self))

    def _prepare_update(self, data):
        if self._adapter.count:
            return self._adapter.create_remote_struct(data)
        else:
            return data

    def _update(self, data):
        raise NotImplementedError()
