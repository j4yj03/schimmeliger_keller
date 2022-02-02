import json
import subprocess as sp
from paho.mqtt import client as mqtt_client
import random
import time

def load_config():
    try:
        conf_file = "./src/conf/config"

        with open(conf_file) as config_file:
            config_data = json.load(config_file)

            print("configuration file",conf_file, "read successful!")

            return config_data

    except Exception as e:
        print(e)

config_data = load_config()
port = config_data['port']
print(port)
file = config_data['file']
print(file)

sp.run(["minicom", "-D", port, "-C", file])
# sp.run(["timeout", "30", "minicom", "-D", port, "-C", file])

# def load_data():
#     try:
#         sensorData_file="./redirect"

#         with open (sensorData_file) as sdf:
#             sdf = json.load
        



# broker = 'io.adafruit.com'
# port = 1883
# topic = "b_ilja/feeds/welcome-feed"
# client_id = f'python-mqtt-{random.randint(0, 1000)}'
# ADAFRUIT_IO_USERNAME = "b_ilja"
# ADAFRUIT_IO_KEY = "aio_FuoS98iogf9JapfSPc4ag1zH9J3o"

# def connect_mqtt():
#     def on_connect(client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT Broker!")
#         else:
#             print("Failed to connect, return code %d\n", rc)
#     # Set Connecting Client ID
#     client = mqtt_client.Client(client_id)
#     client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
#     client.on_connect = on_connect
#     client.connect(broker, port)
#     return client

# def publish(client):
#      while True:
#          time.sleep(10)
#          msg = f"messages: {}"
#          result = client.publish(topic, msg)
#          # result: [0, 1]
#          status = result[0]
#          if status == 0:
#              print(f"Send `{msg}` to topic `{topic}`")
#          else:
#              print(f"Failed to send message to topic {topic}")

# def run():
#     client = connect_mqtt()
#     client.loop_start()
#     publish(client)


# if __name__ == '__main__':
#     run()



