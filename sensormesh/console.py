from datetime import datetime
from .base import Logger


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def update(self, data):
        # Copy input so that original is not modified
        data = dict(data)

        timestamp = data.pop('timestamp', None)
        if timestamp is None:
            str_time = 'None'
        else:
            ts = datetime.fromtimestamp(timestamp)
            str_time = ts.isoformat()

        print(str_time, ':', data)
