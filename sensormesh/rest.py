from .endpoints import DataSource, DataTarget


class RestApi(object):
    @classmethod
    def create_api(cls, api):
        if isinstance(api, dict):
            api = cls(**api)
        elif not api:
            raise ValueError('Missing API input.')
        return api


class RestTarget(DataTarget):
    def __init__(self, api=None, api_cls=RestApi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = api_cls.create_api(api)

    def _update(self, data):
        self._api.post_update(data)


class RestSource(DataSource):
    def __init__(self, api=None, api_cls=RestApi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = api_cls.create_api(api)

    def _read(self):
        return self._api.get_data()
