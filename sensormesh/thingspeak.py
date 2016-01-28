from datetime import datetime
import json

import requests
import dateutil.parser

from .base import DataSource
from .base import Logger
from .exceptions import ConfigurationError


class ThingSpeakEndpoint(DataSource, Logger):
    base_url = 'https://api.thingspeak.com'

    def __init__(self):
        super().__init__()
        self._key = None
        self._channel = None
        self._name = ''
        self._feeds = {}

    @property
    def name(self):
        return self._name

    @property
    def channel(self):
        return self._channel

    def load_config(self, filename):
        with open(filename) as cfg_file:
            cfg_data = json.load(cfg_file)
        self.configure(**cfg_data)

    def read_config(self):
        cfg_data = self.read_info()
        cfg_data.pop('created_at', None)
        cfg_data.pop('updated_at', None)
        cfg_data.pop('last_entry_id', None)

        self.configure(**cfg_data)

    def configure(self, key=None, id=None, name=None, **kwargs):
        if key:
            self._key = key
        if id:
            self._channel = id
        if name:
            self._name = name

        for field, feed in kwargs.items():
            if isinstance(feed, str):
                self._feeds[field] = feed
            else:
                # ignore
                pass

    def read_info(self):
        if not self._channel:
            raise ConfigurationError()

        headers = self.prepare_headers(write=False)
        params = {'results': 0}

        # Fetch data from ThingSpeak
        url = self.base_url + '/channels/' + str(self._channel) + '/feed.json'
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        channel_data = data['channel']

        return channel_data

    def read(self):
        if not self._channel:
            raise ConfigurationError()

        headers = self.prepare_headers(write=False)

        # Fetch data from ThingSpeak
        url = self.base_url + '/channels/' + str(self._channel) + '/feed/last.json'
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return self.parse_feed(response.json())

    def update(self, *args, **kwargs):
        if args:
            raise ValueError()

        headers = self.prepare_headers(write=True)
        values = self.prepare_update(**kwargs)

        # Send data to ThingSpeak
        url = self.base_url + '/update.json'
        response = requests.post(url, headers=headers, json=values)
        response.raise_for_status()

    def parse_feed(self, content):
        ts = dateutil.parser.parse(content['created_at'])
        out = {'timestamp': ts.timestamp()}

        for field, feed in self._feeds.items():
            if field in content:
                out[feed] = content[field]

        return out

    def prepare_update(self, **data):
        values = {}

        for field, feed in self._feeds.items():
            if feed in data:
                values[field] = data[feed]

        if 'timestamp' in data and data['timestamp']:
            timestamp = data['timestamp']
            ts = datetime.fromtimestamp(timestamp)
            values['created_at'] = ts.isoformat()

        return values

    def prepare_headers(self, write=False):
        key = self.get_key(write=write)
        headers = {}
        if key:
            headers['X-THINGSPEAKAPIKEY'] = key

        return headers

    def get_key(self, write=False):
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
