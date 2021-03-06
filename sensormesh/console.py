from datetime import datetime

from .endpoints import DataTarget


class ConsoleDisplay(DataTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update(self, data):
        # Copy input so that original is not modified
        data = dict(data)

        timestamp = data.pop('timestamp', None)
        if timestamp is None:
            str_time = 'None'
        else:
            ts = datetime.fromtimestamp(timestamp)
            str_time = ts.isoformat()

        print(str_time, ':', data)
