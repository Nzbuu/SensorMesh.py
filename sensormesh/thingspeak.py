from datetime import datetime

import requests
import dateutil.parser

from .sensors import Sensor
from .loggers import Logger
from .exceptions import ConfigurationError


class ThingSpeakEndpoint(Sensor, Logger):
    base_url = 'https://api.thingspeak.com'

    def __init__(self):
        super().__init__()
        self.__write_key = None
        self.__read_key = None
        self.__channel = None
        self.__feeds = {}

    def read(self):
        if not self.__channel:
            raise ConfigurationError()

        headers = self.prepare_headers(write=False)

        # Fetch data from ThingSpeak
        url = self.base_url + '/channels/' + str(self.__channel) + '/feed/last.json'
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        print(response.json())
        return self.parse_feed(response.json())

    def update(self, **kwargs):
        headers = self.prepare_headers(write=True)
        values = self.prepare_update(**kwargs)

        # Send data to ThingSpeak
        url = self.base_url + '/update.json'
        response = requests.post(url, headers=headers, json=values)
        response.raise_for_status()

    def parse_feed(self, content):
        ts = dateutil.parser.parse(content['created_at'])
        out = {'timestamp': ts.timestamp()}

        for field, feed in self.__feeds.items():
            if field in content:
                out[feed] = content[field]

        return out

    def prepare_update(self, **kwargs):
        values = {}

        for field, feed in self.__feeds.items():
            if feed in kwargs:
                values[field] = kwargs[feed]

        if 'timestamp' in kwargs and kwargs['timestamp']:
            timestamp = kwargs['timestamp']
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
        if write:
            if self.__write_key:
                return self.__write_key
            else:
                raise ConfigurationError()
        else:
            if self.__read_key:
                return self.__read_key
            elif self.__write_key:
                return self.__write_key
            else:
                return None
