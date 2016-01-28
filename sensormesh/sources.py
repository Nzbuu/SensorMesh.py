class DataSource(object):
    def __init__(self):
        super().__init__()

    def read(self):
        raise NotImplementedError()


class FakeDataSource(DataSource):
    def __init__(self):
        super().__init__()
        self.__value = 0

    def read(self):
        out = self.__value
        self.__value += 1
        return {'count': out}
