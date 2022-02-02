# python3.6

import random

from paho.mqtt import client as mqtt_client


broker = 'io.adafruit.com'
port = 1883
topic = "b_ilja/feeds/welcome-feed"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
ADAFRUIT_IO_USERNAME = "b_ilja"
ADAFRUIT_IO_KEY = "aio_FuoS98iogf9JapfSPc4ag1zH9J3o"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()