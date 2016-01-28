class Logger(object):
    def __init__(self):
        super().__init__()

    def update(self, **kwargs):
        raise NotImplementedError()
