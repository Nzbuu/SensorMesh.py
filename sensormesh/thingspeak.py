from datetime import datetime

import requests
import dateutil.parser

from .base import DataSource, DataAdapter
from .rest import RestTarget
from .exceptions import ConfigurationError


class ThingSpeakApi(object):
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


class ThingSpeakLogger(RestTarget):
    def __init__(self, name='', feeds=None, api=None, **kwargs):
        if api is None:
            api = ThingSpeakApi(**kwargs)
        elif kwargs:
            raise ValueError("Additional keyword inputs are forbidden when using API input")

        super().__init__(name=name, api=api)

        self._adapter = DataAdapter(feeds)

    def _prepare_update(self, data):
        content = self._adapter.parse_local(data)

        if 'timestamp' in data and data['timestamp']:
            timestamp = data['timestamp']
            ts = datetime.fromtimestamp(timestamp)
            content['created_at'] = ts.isoformat()

        return content


class ThingSpeakSource(DataSource):
    def __init__(self, name='', feeds=None, api=None, **kwargs):
        super().__init__(name=name)

        if api is None:
            api = ThingSpeakApi(**kwargs)
        elif kwargs:
            raise ValueError("Additional keyword inputs are forbidden when using API input")
        self._api = api

        self._adapter = DataAdapter(feeds)

    def read(self):
        content = self._api.get_last()
        return self._parse_feed(content)

    def _parse_feed(self, content):
        data = self._adapter.parse_remote(content)

        if 'timestamp' not in data:
            ts = dateutil.parser.parse(content['created_at'])
            data['timestamp'] = ts.timestamp()

        return data
