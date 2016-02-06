from .base import DataTarget
from .exceptions import ConfigurationError


class RestTarget(DataTarget):
    def __init__(self, name='', feeds=None, fields=None, api=None):
        super().__init__(name=name, feeds=feeds, fields=fields)
        self._api = api

    def update(self, data):
        if not self._api:
            raise ConfigurationError()

        content = self._prepare_update(data)
        self._api.post_update(content)

    def _prepare_update(self, data):
        if self._adapter.count:
            return self._adapter.create_remote_struct(data)
        else:
            return data
