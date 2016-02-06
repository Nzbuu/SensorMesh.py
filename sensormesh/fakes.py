from .base import DataSource


class FakeDataSource(DataSource):
    def __init__(self):
        super().__init__()
        self._value = 0
        self._add_field('count')

    def read(self):
        out = self._value
        self._value += 1
        return {'count': out}
