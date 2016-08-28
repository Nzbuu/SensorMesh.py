# -*- coding: utf-8 -*-

from datetime import datetime

import requests
import dateutil.parser

from .endpoints import DataTarget, DataSource, ApiMixin, DataApi
from .exceptions import ConfigurationError


class ThingSpeakApi(DataApi):
    def __init__(self, key=None, channel=None,
                 base_url='https://api.thingspeak.com'):
        super().__init__()
        self._props = {
            'base_url': base_url,
            'key': key,
            'channel': channel,
        }
        self._templates = {
            'update': '{base_url}/update.json',
            'last': '{base_url}/channels/{channel}/feed/last.json',
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
            raise ConfigurationError('Missing channel parameter')

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
        f_str = self._templates[name]
        return f_str.format(**self._props)

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
            raise ConfigurationError('Missing key parameter')
        else:
            return None


class ThingSpeakLogger(ApiMixin, DataTarget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, api_cls=ThingSpeakApi, **kwargs)

    def _prepare_update(self, data):
        data_out = super()._prepare_update(data)

        # created_at has special meaning and should be an ISO date string
        if data_out.get('created_at'):
            timestamp = data_out['created_at']
            if not isinstance(timestamp, str):
                ts = datetime.fromtimestamp(timestamp)
                data_out['created_at'] = ts.isoformat()

        return data_out

    def _update(self, data):
        self._api.post_update(data)


class ThingSpeakSource(ApiMixin, DataSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, api_cls=ThingSpeakApi, **kwargs)

    def _process_data(self, content):
        data = super()._process_data(content)

        # timestamp has special meaning and should be UNIX timestamp in UTC
        if isinstance(data.get('timestamp'), str):
            ts = dateutil.parser.parse(data['timestamp'])
            data['timestamp'] = ts.timestamp()

        return data

    def _read(self):
        return self._api.get_data()
