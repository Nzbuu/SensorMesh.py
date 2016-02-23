import tweepy

from .rest import RestTarget, RestApi


class TwitterApi(RestApi):
    def __init__(self, consumer_token=None, consumer_secret=None,
                 access_token=None, access_token_secret=None):
        super().__init__()

        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self._api = tweepy.API(auth)

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
