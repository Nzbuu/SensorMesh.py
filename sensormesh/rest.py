import logging

from .endpoints import DataSource, DataTarget, ApiMixin

logger = logging.getLogger(__name__)


class RestTarget(ApiMixin, DataTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _update(self, data):
        self._api.post_update(data)


class RestSource(ApiMixin, DataSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read(self):
        return self._api.get_data()
