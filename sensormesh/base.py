class DataSource(object):
    def __init__(self):
        super().__init__()

    def read(self):
        raise NotImplementedError()


class DataTarget(object):
    def __init__(self):
        super().__init__()

    def update(self, data):
        raise NotImplementedError()


class DataSourceWrapper(DataSource):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if args:
            raise ValueError()

        self._dict = kwargs

    def read(self):
        data = {k: v() for k, v in self._dict.items()}
        return data
