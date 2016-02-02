from datetime import datetime
from .base import Logger


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def update(self, data):
        timestamp = data.get('timestamp', None)
        if timestamp is None:
            str_time = 'None'
        else:
            ts = datetime.fromtimestamp(timestamp)
            str_time = ts.isoformat()

        print(str_time, ':', data)
