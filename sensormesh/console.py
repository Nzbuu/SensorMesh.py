from datetime import datetime
from .loggers import Logger


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def update(self, timestamp=None, **kwargs):
        print(datetime.fromtimestamp(timestamp).isoformat(), ':', kwargs)
