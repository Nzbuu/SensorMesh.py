from .endpoints import DataTarget
from .exceptions import ConfigurationError


class RestTarget(DataTarget):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
