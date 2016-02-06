import csv
import os.path

from .base import DataTarget


class TextLogger(DataTarget):
    def __init__(self, filename, name=''):
        super().__init__(name=name)
        self._filename = filename

    def update(self, data):
        did_exist = os.path.isfile(self._filename)
        with open(self._filename, 'a') as fp:
            csv_file = csv.DictWriter(fp, fieldnames=data.keys())
            if not did_exist:
                csv_file.writeheader()
            csv_file.writerow(data)

    def __del__(self):
        pass
