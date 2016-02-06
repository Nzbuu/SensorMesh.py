from datetime import datetime
from string import Template

import requests
import dateutil.parser

from .base import DataSource
from .rest import RestTarget
from .utils import DataAdapter
from .exceptions import ConfigurationError


class ThingSpeakApi(object):
    def __init__(self, key=None, channel=None,
                 base_url='https://api.thingspeak.com'):
        super().__init__()
        self._props = {
            'base_url': base_url,
            'key': key,
            'channel': channel,
        }
        self._templates = {
            'update': Template(r'$base_url/update.json'),
            'last': Template(r'$base_url/channels/$channel/feed/last.json'),
        }

    @property
    def base_url(self):
        return self._props['base_url']

    @property
    def key(self):
        return self._props['key']

    @property
    def channel(self):
        return self._props['channel']

    def get_data(self):
        if not self.channel:
            raise ConfigurationError()

        headers = self._prepare_headers(write=False)

        # Fetch data from ThingSpeak
        url = self._get_url('last')
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        return response.json()

    def post_update(self, content):
        headers = self._prepare_headers(write=True)

        # Send data to ThingSpeak
        url = self._get_url('update')
        response = requests.post(url, headers=headers, json=content)
        response.raise_for_status()

    def _get_url(self, name):
        t = self._templates[name]
        return t.substitute(self._props)

    def _prepare_headers(self, write=False):
        key = self._get_key(write=write)
        headers = {}
        if key:
            headers['X-THINGSPEAKAPIKEY'] = key

        return headers

    def _get_key(self, write=False):
        if self.key:
            return self.key
        elif write:
            raise ConfigurationError()
        else:
            return None


class ThingSpeakLogger(RestTarget):
    def __init__(self, name='', feeds=None, api=None, **kwargs):
        if api is None:
            api = ThingSpeakApi(**kwargs)
        elif kwargs:
            raise ValueError(
                    "Additional keyword inputs are forbidden when using "
                    "API input")

        super().__init__(name=name, api=api)

        if feeds:
            for remote_name, local_name in feeds.items():
                self._add_field(
                        local_name=local_name,
                        remote_name=remote_name)

    def _prepare_update(self, data):
        content = self._adapter.create_remote_struct(data)

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
            raise ValueError(
                    "Additional keyword inputs are forbidden when using "
                    "API input")
        self._api = api

        if feeds:
            for remote_name, local_name in feeds.items():
                self._add_field(
                        local_name=local_name,
                        remote_name=remote_name)

    def read(self):
        content = self._api.get_data()
        return self._parse_feed(content)

    def _parse_feed(self, content):
        data = self._adapter.create_local_struct(content)

        if 'timestamp' not in data:
            ts = dateutil.parser.parse(content['created_at'])
            data['timestamp'] = ts.timestamp()

        return data
