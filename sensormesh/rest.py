import inspect

from .endpoints import DataTarget


class RestApi(object):
    @classmethod
    def configure_api(cls, api=None, kwargs=None):
        if not kwargs:
            kwargs = {}

        # Get API instance class
        if api:
            api_cls = api.__class__
        else:
            api_cls = cls

        # Extract API configuration parameters from kwargs
        sig = inspect.signature(api_cls.__init__)
        config_api = {k: kwargs.pop(k) for k in sig.parameters if k in kwargs}

        # Create API instance
        if api:
            if config_api:
                raise TypeError('Cannot specify API object and API parameters')
        else:
            api = api_cls(**config_api)

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
