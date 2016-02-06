from .utils import DataAdapter
from .exceptions import ConfigurationError


class Base(object):
    def __init__(self, name='', feeds=None, fields=None):
        if feeds and fields:
            raise TypeError('Only use one of feeds or fields')

        super().__init__()
        self._name = name
        self._adapter = DataAdapter()

        if fields:
            for name in fields:
                if isinstance(name, str):
                    self._adapter.add_field(name, name)
                else:
                    self._adapter.add_field(
                            local_name=name[0],
                            remote_name=name[1])
        elif feeds:
            for remote_name, local_name in feeds.items():
                self._adapter.add_field(
                        local_name=local_name,
                        remote_name=remote_name
                )

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
    def __init__(self, name='', feeds=None, fields=None):
        super().__init__(name=name, feeds=feeds, fields=fields)

    def read(self):
        raise NotImplementedError()


class DataTarget(Base):
    def __init__(self, name='', feeds=None, fields=None):
        super().__init__(name=name, feeds=feeds, fields=fields)

    def update(self, data):
        raise NotImplementedError()


class DataSourceWrapper(DataSource):
    def __init__(self, name='', feeds=None, fields=None, source=()):
        if not feeds and not fields:
            fields = ['value']

        super().__init__(name=name, feeds=feeds, fields=fields)

        if not source:
            raise ConfigurationError

        self._source = None
        self._dict = {}

        if callable(source):
            self._source = source
            for name in fields:
                self._add_field(name)
                self._dict[name] = None
        else:
            for name, src in zip(fields, source):
                self._add_field(name)
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
