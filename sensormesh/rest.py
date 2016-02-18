import inspect

from .endpoints import DataSource, DataTarget


class RestApi(object):
    @classmethod
    def configure_api(cls, api):
        if isinstance(api, dict):
            api = cls(**api)

        return api


class RestTarget(DataTarget):
    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if api:
            self._api = api
        else:
            raise ValueError('Missing API input.')

    def _update(self, data):
        self._api.post_update(data)


class RestSource(DataSource):
    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if api:
            self._api = api
        else:
            raise ValueError('Missing API input.')

    def _read(self):
        return self._api.get_data()
