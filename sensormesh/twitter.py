import tweepy

from .endpoints import DataApi
from .rest import RestTarget


class TwitterApi(DataApi):
    def __init__(self, consumer_token=None, consumer_secret=None,
                 access_token=None, access_token_secret=None):
        super().__init__()

        self._props = {
            'consumer_token': consumer_token,
            'consumer_secret': consumer_secret,
            'access_token': access_token,
            'access_token_secret': access_token_secret,
        }
        self._api = None

    def open(self):
        super().open()

        # Create OAuth handler
        auth = tweepy.OAuthHandler(
            self._props['consumer_token'], self._props['consumer_secret'])
        auth.set_access_token(
            self._props['access_token'], self._props['access_token_secret'])

        # Create tweepy API instance
        self._api = tweepy.API(auth)

    def close(self):
        self._api = None
        super().close()

    def post_update(self, data):
        self._api.update_status(status=data['message'])


class TwitterUpdate(RestTarget):
    def __init__(self, message='', *args, **kwargs):
        super().__init__(*args, api_cls=TwitterApi, **kwargs)
        self._message = message

    def _prepare_update(self, data):
        data_out = super()._prepare_update(data)
        data_out['message'] = self._message.format(**data_out)
        return data_out
