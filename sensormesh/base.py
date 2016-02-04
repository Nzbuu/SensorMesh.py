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


class DataAdapter(object):
    def __init__(self, feeds=None):
        super().__init__()

        self._local_names = {}
        self._remote_names = {}
        if feeds:
            self.add_field(**feeds)

    def add_field(self, **kwargs):
        for remote_name, local_name in kwargs.items():
            if remote_name in self._local_names:
                if self._local_names[remote_name] == local_name:
                    # already have remote_name <-> local_name
                    pass
                else:
                    # already have remote_name but doesn't correspond to local_name
                    raise KeyError('Local and Remote names must be unique.')
            elif local_name in self._remote_names:
                    # already have local_name but doesn't correspond to remote_name
                raise KeyError('Local and Remote names must be unique.')
            else:
                self._local_names[remote_name] = local_name
                self._remote_names[local_name] = remote_name

    def parse_local(self, local_data):
        return self._rename_fields(local_data, self._remote_names)

    def parse_remote(self, remote_data):
        return self._rename_fields(remote_data, self._local_names)

    def _rename_fields(self, data, names):
        return {names[k]: data[k] for k in names if k in data}
