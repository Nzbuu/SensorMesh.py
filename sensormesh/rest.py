from .base import DataTarget
from .exceptions import ConfigurationError


class RestTarget(DataTarget):
    def __init__(self, name='', feeds=None, fields=None, api=None):
        super().__init__(name=name, feeds=feeds, fields=fields)

        if api:
            self._api = api
        else:
            raise ConfigurationError()

    def update(self, data):
        content = self._prepare_update(data)
        self._api.post_update(content)

    def _prepare_update(self, data):
        if self._adapter.count:
            return self._adapter.create_remote_struct(data)
        else:
            return data
