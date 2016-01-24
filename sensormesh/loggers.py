from datetime import datetime


class Logger(object):
    def __init__(self):
        pass

    def add(self, time=None, **kwargs):
        pass


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def add(self, time=None, **kwargs):
        print(datetime.fromtimestamp(time), ':', kwargs)
