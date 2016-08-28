# -*- coding: utf-8 -*-

import tweepy

from .endpoints import ApiMixin, DataTarget, DataApi


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
        self._client = None

    def open(self):
        super().open()

        # Create OAuth handler
        auth = tweepy.OAuthHandler(
            self._props['consumer_token'], self._props['consumer_secret'])
        auth.set_access_token(
            self._props['access_token'], self._props['access_token_secret'])

        # Create tweepy API instance
        self._client = tweepy.API(auth)

    def close(self):
        self._client = None
        super().close()

    def post_update(self, message):
        self._client.update_status(status=message)


class TwitterUpdate(ApiMixin, DataTarget):
    def __init__(self, message='', *args, **kwargs):
        super().__init__(*args, api_cls=TwitterApi, **kwargs)
        self._message = message

    def _update(self, data):
        message = self._message.format(**data)
        self._api.post_update(message)
