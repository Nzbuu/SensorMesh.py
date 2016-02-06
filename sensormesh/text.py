import csv
import os.path

from .base import DataTarget


class TextLogger(DataTarget):
    def __init__(self, filename, feeds=None, fields=None, name=''):
        if not feeds and not fields:
            raise TypeError('Missing fields or feeds information')

        super().__init__(name=name, feeds=feeds, fields=fields)
        self._filename = filename
        self._adapter.create_missing = True

    @property
    def filename(self):
        return self._filename

    def update(self, data):
        content = self._adapter.create_remote_struct(data)

        did_exist = os.path.isfile(self._filename)
        with open(self._filename, 'a') as fp:
            csv_file = csv.DictWriter(
                    fp,
                    fieldnames=list(self._adapter.remote_names),
            )
            if not did_exist:
                csv_file.writeheader()

            csv_file.writerow(content)
