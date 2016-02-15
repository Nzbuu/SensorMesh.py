from .endpoints import DataSource


class DataSourceWrapper(DataSource):
    def __init__(self, source=None, *args, **kwargs):
        if 'fields' not in kwargs:
            kwargs['fields'] = ('value',)
        super().__init__(*args, **kwargs)

        if not source:
            raise ValueError('Missing source input')
        self._source = source

    def _read(self):
        values = self._source()
        if len(self.fields_remote) == 1:
            data = {self.fields_remote[0]: values}
        else:
            data = {name: value
                    for name, value in zip(self.fields_remote, values)}

        return data
