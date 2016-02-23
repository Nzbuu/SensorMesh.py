import logging

from .endpoints import DataSource, DataTarget, DataEndpoint

logger = logging.getLogger(__name__)


class RestApi(object):
    @classmethod
    def create_api(cls, api):
        if isinstance(api, dict):
            api = cls(**api)
        elif not api:
            raise ValueError('Missing API input.')
        return api

    def open(self):
        logger.info('Opening %s', self)

    def close(self):
        logger.info('Closing %s', self)

    def __str__(self):
        return '{0}()'.format(self.__class__.__name__)


class ApiMixin(DataEndpoint):
    def __init__(self, api=None, api_cls=RestApi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._api = api_cls.create_api(api)

    def open(self):
        super().open()
        self._api.open()

    def close(self):
        self._api.close()
        super().close()


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
