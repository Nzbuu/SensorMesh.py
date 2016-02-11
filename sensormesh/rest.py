from .endpoints import DataTarget
from .exceptions import ConfigurationError


class RestTarget(DataTarget):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if api:
            self._api = api
        else:
            raise ConfigurationError()

    def _update(self, data):
        self._api.post_update(data)
