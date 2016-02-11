from .utils import DataAdapter
from .exceptions import ConfigurationError


class DataEndpoint(object):
    def __init__(self, name='', fields=None):
        super().__init__()
        self._name = name
        self._adapter = DataAdapter()

        if fields:
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

    def _add_field(self, local_name, remote_name=None):
        if not remote_name:
            remote_name = local_name

        self._adapter.add_field(
                local_name=local_name,
                remote_name=remote_name
        )

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        pass

    def close(self):
        pass


class DataSource(DataEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read(self):
        raise NotImplementedError()


class DataTarget(DataEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, data):
        data_out = self._prepare_update(data)
        self._update(data_out)

    def _prepare_update(self, data):
        if self._adapter.count:
            return self._adapter.create_remote_struct(data)
        else:
            return data

    def _update(self, data):
        raise NotImplementedError()


class DataSourceWrapper(DataSource):
    def __init__(self, source=(), *args, **kwargs):
        if 'fields' not in kwargs:
            kwargs['fields'] = ('value',)
        super().__init__(*args, **kwargs)

        if not source:
            raise ConfigurationError

        self._source = None
        self._dict = {}

        if callable(source):
            self._source = source
            for name in self.fields:
                self._dict[name] = None
        else:
            for name, src in zip(self.fields, source):
                self._dict[name] = src

    def read(self):
        if self._source:
            values = self._source()
            if len(self.fields) == 1:
                data = {self.fields[0]: values}
            else:
                data = {name: value
                        for name, value in zip(self.fields, values)}
        else:
            data = {name: source() for name, source in self._dict.items()}

        return data
