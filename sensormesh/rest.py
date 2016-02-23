from .endpoints import DataSource, DataTarget


class RestApi(object):
    @classmethod
    def create_api(cls, api):
        if isinstance(api, dict):
            api = cls(**api)
        elif not api:
            raise ValueError('Missing API input.')
        return api


class ApiMixin(object):
    def __init__(self, api=None, api_cls=RestApi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = api_cls.create_api(api)


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
