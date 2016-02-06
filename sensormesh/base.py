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
    def __init__(self, name='', *args, **kwargs):
        super().__init__(name=name)
        if args:
            raise ValueError()

        self._dict = kwargs

    def read(self):
        data = {k: v() for k, v in self._dict.items()}
        return data
