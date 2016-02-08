from .utils import DataAdapter
from .exceptions import ConfigurationError


class Base(object):
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

    @name.setter
    def name(self, u):
        self._name = u

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


class DataSource(Base):
    def __init__(self, name='', fields=None):
        super().__init__(name=name, fields=fields)

    def read(self):
        raise NotImplementedError()


class DataTarget(Base):
    def __init__(self, name='', fields=None):
        super().__init__(name=name, fields=fields)

    def update(self, data):
        raise NotImplementedError()


class DataSourceWrapper(DataSource):
    def __init__(self, name='', fields=('value',), source=()):
        super().__init__(name=name, fields=fields)

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
