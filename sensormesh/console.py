from datetime import datetime
from .loggers import Logger


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def add(self, time=None, **kwargs):
        print(datetime.fromtimestamp(time).isoformat(), ':', kwargs)
