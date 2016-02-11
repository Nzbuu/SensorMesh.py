import csv
import os.path

from .endpoints import DataTarget


class TextLogger(DataTarget):
    def __init__(self, filename, fields, reopen_file=True, *args, **kwargs):
        super().__init__(*args, fields=fields, **kwargs)
        self._filename = filename
        self._reopen = reopen_file
        self._adapter.create_missing = True
        self._file = None
        self._writer = None

    @property
    def filename(self):
        return self._filename

    def open(self):
        if not self._file:
            create_file = not(self._reopen and os.path.isfile(self._filename))
            file_mode = 'w' if create_file else 'a'

            self._file = open(self._filename, file_mode, newline='')
            self._writer = csv.DictWriter(
                    self._file,
                    fieldnames=list(self._adapter.remote_names),
            )
            if create_file:
                self._writer.writeheader()

    def close(self):
        if self._file:
            self._writer = None

            f = self._file
            self._file = None
            f.close()

    def update(self, data):
        content = self._adapter.create_remote_struct(data)
        self._writer.writerow(content)
