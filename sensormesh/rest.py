from .base import DataTarget
from .exceptions import ConfigurationError


class RestTarget(DataTarget):
    def __init__(self, name='', api=None):
        super().__init__(name=name)
        self._api = api

    def update(self, data):
        if not self._api:
            raise ConfigurationError()

        content = self._prepare_update(data)
        self._api.post_update(content)

    def _prepare_update(self, data):
        return data
