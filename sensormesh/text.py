import csv
import os.path

from .base import DataTarget


class TextLogger(DataTarget):
    def __init__(self, filename, feeds, name=''):
        super().__init__(name=name)
        self._filename = filename

        for name in feeds:
            self._add_field(name)

    @property
    def filename(self):
        return self._filename

    def update(self, data):
        did_exist = os.path.isfile(self._filename)
        with open(self._filename, 'a') as fp:
            csv_file = csv.DictWriter(
                    fp,
                    fieldnames=self.fields,
                    extrasaction='ignore'
            )
            if not did_exist:
                csv_file.writeheader()

            csv_file.writerow(data)

    def __del__(self):
        pass
