from .endpoints import DataTarget


class RestTarget(DataTarget):
    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if api:
            self._api = api
        else:
            raise ValueError('Missing API input.')

    def _update(self, data):
        self._api.post_update(data)
