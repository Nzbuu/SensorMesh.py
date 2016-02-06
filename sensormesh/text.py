import csv
import os.path

from .base import DataTarget


class TextLogger(DataTarget):
    def __init__(self, filename, fields, name=''):
        super().__init__(name=name, fields=fields)
        self._filename = filename
        self._adapter.create_missing = True

    @property
    def filename(self):
        return self._filename

    def update(self, data):
        content = self._adapter.create_remote_struct(data)

        did_exist = os.path.isfile(self._filename)
        with open(self._filename, 'a', newline='') as fp:
            csv_file = csv.DictWriter(
                    fp,
                    fieldnames=list(self._adapter.remote_names),
            )
            if not did_exist:
                csv_file.writeheader()

            csv_file.writerow(content)
