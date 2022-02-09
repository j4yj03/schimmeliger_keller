import json
from paho.mqtt import client as mqtt_client
import random

from serial import Serial

broker = 'io.adafruit.com'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'

global ADAFRUIT_IO_TOPICS 

global ADAFRUIT_IO_USERNAME
global ADAFRUIT_IO_KEY

global TRESH_TEMP_H
global TRESH_TEMP_L
global TRESH_HUM_H
global TRESH_HUM_L



def read_config():
    fn = "./config/conf.json"

    with open(fn) as config_file:
        config_data = json.load(config_file)

        print("configuration file", fn, "read successful!")

        ADAFRUIT_IO_USERNAME = config_data['adafruit']['user']
        ADAFRUIT_IO_KEY = config_data['adafruit']['key']
        ADAFRUIT_IO_TOPICS_LIST = config_data['adafruit']['topics']

        TRESH_TEMP_H = config_data['adafruit']['threshhold_temp_high']
        TRESH_TEMP_L = config_data['adafruit']['threshhold_temp_low']
        TRESH_HUM_H = config_data['adafruit']['threshhold_hum_high']
        TRESH_HUM_L = config_data['adafruit']['threshhold_hum_low']

def read_data():
    try:
        ser = Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
    except Exception as e:
            print("Error: ", e)
        
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
                    
                    if (-40.0 < float(temp) < 80.0) and (0.0 < float(hum) < 100.0): #DHT22 range
                        return temp, hum, dev_ID

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

def publish(client, topic, msg):
    msg = f"{msg}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    
if __name__ == '__main__':

    try:

        read_config()

        client = connect_mqtt()
        client.loop_start()
    except Exception as e:
        print(e)

    while True:
        temp, hum, dev_ID = read_data()

        if TRESH_TEMP_L < temp < TRESH_TEMP_H:
            publish(client, ADAFRUIT_IO_TOPICS_LIST[0], temp)

        else:
            publish(client, ADAFRUIT_IO_TOPICS_LIST[2], temp)

        if TRESH_HUM_L < hum < TRESH_HUM_H:
            publish(client, ADAFRUIT_IO_TOPICS_LIST[1], hum)

        else:
            publish(client, ADAFRUIT_IO_TOPICS_LIST[3], hum)
    



