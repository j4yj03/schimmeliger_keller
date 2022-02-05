from curses import baudrate
import json
import subprocess as sp
from paho.mqtt import client as mqtt_client
import random
import time
from datetime import datetime
import sys
import serial

broker = 'io.adafruit.com'
port = 1883
topics = ["b_ilja/feeds/temperature", "b_ilja/feeds/humidity", "b_ilja/feeds/alarm_temp", "b_ilja/feeds/alarm_hum"]
client_id = f'python-mqtt-{random.randint(0, 1000)}'
ADAFRUIT_IO_USERNAME = "b_ilja"
ADAFRUIT_IO_KEY = "aio_FuoS98iogf9JapfSPc4ag1zH9J3o"

def read_data():
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
    time_old = 0
    while True:
        try:
            data_str = ser.readline().decode('ascii')
            if len(data_str) > 0:
                data_dict = json.loads(data_str)
                print(data_dict)
                time_current = data_dict["time"]
                if time_current > time_old:
                    time_old = time_current
                    temp = data_dict["temp"] 
                    hum = data_dict["hum"] 
                    dev_ID = data_dict["devID"]
                    
                    return [temp, hum], dev_ID

        except Exception as e:
            print("Error: " + str(e))


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client,topic, msg):
    msg = f"{msg}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    
if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()
    while True:
        sensor_values, dev_ID = read_data()
        for value, topic in zip(sensor_values, topics):
            publish(client, topic, value)
    



