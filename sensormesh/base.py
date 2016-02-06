from .exceptions import ConfigurationError


class DataSource(object):
    def __init__(self, name=''):
        super().__init__()
        self._name = name
        self._fields = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, u):
        self._name = u

    @property
    def fields(self):
        return self._fields

    def _add_field(self, name_local):
        self._fields.append(name_local)

    def read(self):
        raise NotImplementedError()


class DataTarget(object):
    def __init__(self, name=''):
        super().__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, u):
        self._name = u

    def update(self, data):
        raise NotImplementedError()


class DataSourceWrapper(DataSource):
    def __init__(self, name='', fields=(), source=()):
        super().__init__(name=name)

        if not source:
            raise ConfigurationError

        self._source = None
        self._dict = {}

        if callable(source):
            self._source = source
            for n in fields:
                self._add_field(n)
                self._dict[n] = None
        else:
            for n, s in zip(fields, source):
                self._add_field(n)
                self._dict[n] = s

    def read(self):
        if self._source:
            values = self._source()
            if len(self._fields) == 1:
                data = {self._fields[0]: values}
            else:
                data = {name: value for name, value in zip(self._fields, values)}
        else:
            data = {name: source() for name, source in self._dict.items()}

        return data
