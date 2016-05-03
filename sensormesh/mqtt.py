import json
import logging
from urllib.parse import urlsplit

import paho.mqtt.client as mqtt

from .endpoints import DataTarget, DataApi, ApiMixin

logger = logging.getLogger(__name__)
log_level_std = {
    mqtt.MQTT_LOG_INFO: logging.INFO,
    mqtt.MQTT_LOG_NOTICE: logging.INFO,  # No direct equivalent
    mqtt.MQTT_LOG_WARNING: logging.WARNING,
    mqtt.MQTT_LOG_ERR: logging.ERROR,
    mqtt.MQTT_LOG_DEBUG: logging.DEBUG,
}


class MqttApi(DataApi):
    def __init__(self, url, client_id=None,
                 username=None, password=None,
                 keepalive=60):
        super().__init__()

        url_parts = urlsplit(url)
        self._props = {
            'client_id': client_id,
            'host': url_parts.hostname,
            'port': url_parts.port or 1883,
            'username': username or url_parts.username,
            'password': password or url_parts.password,
            'keepalive': keepalive,
        }
        self._client = None

    def open(self):
        super().open()

        self._client = self._prepare_client()

        logger.info("Connecting: %s:%d",
                    self._props['host'], self._props['port'])
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
        if self._props['username']:
            client.username_pw_set(
                self._props['username'], self._props['password'])

        client.on_log = self._handle_mqtt_log
        client.on_connect = self._handle_mqtt_connect
        client.on_disconnect = self._handle_mqtt_disconnect
        client.on_publish = self._handle_mqtt_publish

        return client

    def _handle_mqtt_log(self, client, userdata, level, string):  # pylint: disable=W6013,R0201
        logger.log(log_level_std[level], string)

    def _handle_mqtt_connect(self, client, userdata, flags, rc):  # pylint: disable=W6013,R0201
        logger.info("Connected: %s:%d result=%d %s",
                    client._host, client._port, rc, flags)  # pylint: disable=W0212

    def _handle_mqtt_disconnect(self, client, userdata, rc):  # pylint: disable=W6013,R0201
        logger.info("Disconnected: %s:%d result=%d",
                    client._host, client._port, rc)  # pylint: disable=W0212

    def _handle_mqtt_publish(self, client, userdata, mid):  # pylint: disable=W6013,R0201
        logger.info("Published: mid=%d", mid)


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
