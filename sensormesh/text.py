# -*- coding: utf-8 -*-

import csv
import os.path
import logging

from .endpoints import DataTarget

logger = logging.getLogger(__name__)


class TextLogger(DataTarget):
    def __init__(self, filename, fields, mode='a', *args, **kwargs):
        super().__init__(*args, fields=fields, **kwargs)
        self._filename = filename

        if mode in {'a', 'w'}:
            self._filemode = mode
        else:
            raise ValueError('Invalid file mode')

        self._adapter.create_missing = True
        self._file = None
        self._writer = None

    @property
    def filename(self):
        return self._filename

    @property
    def mode(self):
        return self._filemode

    def open(self):
        super().open()
        if not self._file:
            create_file = (self._filemode == 'w' or
                           not os.path.isfile(self._filename))

            self._file = open(self._filename, self._filemode, newline='')
            self._writer = csv.DictWriter(
                self._file,
                fieldnames=list(self._adapter.remote_names),
            )
            if create_file:
                logger.info('Creating %r for %s', self._filename, self)
                self._writer.writeheader()

    def close(self):
        super().close()
        if self._file:
            self._writer = None

            f = self._file
            self._file = None
            f.close()

    def _update(self, data):
        self._writer.writerow(data)

    def __str__(self):
        return "{0}(name={1!r}, filename={2!r})".format(
            self.__class__.__name__,
            self._name,
            self._filename
        )
