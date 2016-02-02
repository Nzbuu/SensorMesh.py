class DataSource(object):
    def __init__(self, name=''):
        super().__init__()
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, u):
        self._name = u

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
