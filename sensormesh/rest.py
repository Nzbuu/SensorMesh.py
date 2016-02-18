import inspect

from .endpoints import DataSource, DataTarget


class RestApi(object):
    pass


class RestTarget(DataTarget):
    def __init__(self, api=None, api_cls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(api, dict):
            self._api = api_cls(**api)
        elif api:
            self._api = api
        else:
            raise ValueError('Missing API input.')

    def _update(self, data):
        self._api.post_update(data)


class RestSource(DataSource):
    def __init__(self, api=None, api_cls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if isinstance(api, dict):
            self._api = api_cls(**api)
        elif api:
            self._api = api
        else:
            raise ValueError('Missing API input.')

    def _read(self):
        return self._api.get_data()
