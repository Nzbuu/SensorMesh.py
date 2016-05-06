import json
from urllib.parse import urlsplit

import paho.mqtt.client as mqtt

from .endpoints import DataTarget, DataApi, ApiMixin


class MqttApi(DataApi):
    def __init__(self, url, client_id=None,
                 keepalive=60):
        super().__init__()

        o = urlsplit(url)
        self._props = {
            'client_id': client_id,
            'host': o.hostname,
            'port': o.port or 1883,
            'keepalive': keepalive,
        }
        self._client = None

    def open(self):
        super().open()

        self._client = self._prepare_client()

        self._client.connect(host=self._props['host'], port=self._props['port'],
                             keepalive=self._props['keepalive'])
        self._client.loop_start()

    def close(self):
        self._client.loop_stop()
        self._client.disconnect()
        self._client = None

        super().close()

    def publish(self, topic, data, *args, **kwargs):
        self._client.publish(topic=topic, payload=data, *args, **kwargs)

    def _prepare_client(self):
        # Create MQTT client API instance
        client = mqtt.Client(
            client_id=self._props['client_id'],
            clean_session=True,
        )
        return client


class MqttUpdate(ApiMixin, DataTarget):
    def __init__(self, topic, qos=0, *args, **kwargs):
        super().__init__(*args, api_cls=MqttApi, **kwargs)
        self._topic = topic
        self._qos = qos

    def _update(self, data):
        self._api.publish(
            topic=self._topic,
            data=json.dumps(data),
            qos=self._qos,
            retain=False,
        )

    def __str__(self):
        return "{0}(name={1!r}, topic={2!r})".format(
            self.__class__.__name__, self._name, self._topic)
