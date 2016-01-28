class Logger(object):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        if args:
            raise ValueError()
        raise NotImplementedError()
