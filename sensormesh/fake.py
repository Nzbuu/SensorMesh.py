from .base import DataSource


class FakeDataSource(DataSource):
    def __init__(self):
        super().__init__()
        self.__value = 0

    def read(self):
        out = self.__value
        self.__value += 1
        return {'count': out}
