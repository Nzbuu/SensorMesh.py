from datetime import datetime

import requests
import dateutil.parser

from .base import DataSource
from .base import DataTarget
from .exceptions import ConfigurationError


class ThingSpeakApi:
    def __init__(self, key=None, channel=None, base_url='https://api.thingspeak.com'):
        super().__init__()
        self._base_url = base_url
        self._key = key
        self._channel = channel

    def get_last(self):
        if not self._channel:
            raise ConfigurationError()

        headers = self._prepare_headers(write=False)

        # Fetch data from ThingSpeak
        url = self._base_url + '/channels/' + str(self._channel) + '/feed/last.json'
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    def post_update(self, content):
        headers = self._prepare_headers(write=True)

        # Send data to ThingSpeak
        url = self._base_url + '/update.json'
        response = requests.post(url, headers=headers, json=content)
        response.raise_for_status()

    def _prepare_headers(self, write=False):
        key = self._get_key(write=write)
        headers = {}
        if key:
            headers['X-THINGSPEAKAPIKEY'] = key

        return headers

    def _get_key(self, write=False):
        if self._key:
            return self._key
        elif write:
            raise ConfigurationError()
        else:
            return None


class ThingSpeakEndpoint(DataSource, DataTarget):
    def __init__(self, name='', feeds=None, api=None, **kwargs):
        super().__init__(name=name)

        if api is None:
            api = ThingSpeakApi(**kwargs)

        self._api = api
        self._feeds = {}
        if feeds:
            self.add_field(**feeds)

    def add_field(self, **kwargs):
        for field, feed in kwargs.items():
            self._feeds[field] = feed


class ThingSpeakLogger(ThingSpeakEndpoint):
    def update(self, data):
        content = self._prepare_update(data)
        self._api.post_update(content)

    def _prepare_update(self, data):
        values = {field: data[feed] for field, feed in self._feeds.items() if feed in data}

        if 'timestamp' in data and data['timestamp']:
            timestamp = data['timestamp']
            ts = datetime.fromtimestamp(timestamp)
            values['created_at'] = ts.isoformat()

        return values


class ThingSpeakSource(ThingSpeakEndpoint):
    def read(self):
        content = self._api.get_last()
        return self._parse_feed(content)

    def _parse_feed(self, content):
        data = {feed: content[field] for field, feed in self._feeds.items() if field in content}

        if 'timestamp' not in data:
            ts = dateutil.parser.parse(content['created_at'])
            data['timestamp'] = ts.timestamp()

        return data
