class DataSource(object):
    def __init__(self):
        super().__init__()

    def read(self):
        raise NotImplementedError()


class Logger(object):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        raise NotImplementedError()
