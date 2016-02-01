from datetime import datetime
import json

import requests
import dateutil.parser

from .base import DataSource
from .base import Logger
from .exceptions import ConfigurationError


class ThingSpeakEndpoint(DataSource, Logger):
    def __init__(self, key=None, channel=None, name='', feeds=None,
                 base_url='https://api.thingspeak.com'):
        super().__init__()

        self._base_url = base_url
        self._key = key
        self._channel = channel
        self._name = name

        self._feeds = {}
        if feeds:
            self.add_field(**feeds)

    @property
    def name(self):
        return self._name

    @property
    def channel(self):
        return self._channel

    def add_field(self, **kwargs):
        for field, feed in kwargs.items():
            self._feeds[field] = feed

    @classmethod
    def from_file(cls, filename):
        with open(filename) as cfg_file:
            cfg_data = json.load(cfg_file)
        cls(**cfg_data)

    def read_config(self):
        info = self.read_info()
        for k, v in info.items():
            if k == 'name':
                self._name = v
            elif k.startswith('field'):
                self.add_field(**{k: v})
            else:
                pass

    def read_info(self):
        if not self._channel:
            raise ConfigurationError()

        headers = self._prepare_headers(write=False)
        params = {'results': 0}

        # Fetch data from ThingSpeak
        url = self._base_url + '/channels/' + str(self._channel) + '/feed.json'
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        channel_data = data['channel']

        return channel_data

    def read(self):
        if not self._channel:
            raise ConfigurationError()

        headers = self._prepare_headers(write=False)

        # Fetch data from ThingSpeak
        url = self._base_url + '/channels/' + str(self._channel) + '/feed/last.json'
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return self._parse_feed(response.json())

    def update(self, data):
        headers = self._prepare_headers(write=True)
        values = self._prepare_update(data)

        # Send data to ThingSpeak
        url = self._base_url + '/update.json'
        response = requests.post(url, headers=headers, json=values)
        response.raise_for_status()

    def _parse_feed(self, content):
        data = {feed: content[field] for field, feed in self._feeds.items() if field in content}

        if 'timestamp' not in data:
            ts = dateutil.parser.parse(content['created_at'])
            data['timestamp'] = ts.timestamp()

        return data

    def _prepare_update(self, data):
        values = {field: data[feed] for field, feed in self._feeds.items() if feed in data}

        if 'timestamp' in data and data['timestamp']:
            timestamp = data['timestamp']
            ts = datetime.fromtimestamp(timestamp)
            values['created_at'] = ts.isoformat()

        return values

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


class ThingSpeakLogger(ThingSpeakEndpoint):
    pass


class ThingSpeakSource(ThingSpeakEndpoint):
    pass
