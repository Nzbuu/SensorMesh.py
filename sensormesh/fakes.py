from .base import DataSource


class FakeDataSource(DataSource):
    def __init__(self):
        super().__init__(fields=('count',))
        self._value = 0

    def read(self):
        out = self._value
        self._value += 1
        return {'count': out}
