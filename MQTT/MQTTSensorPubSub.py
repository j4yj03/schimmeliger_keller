import json
from datetime import datetime
from paho.mqtt import client as mqtt_client
import random

from serial import Serial

class MQTTSensorPubSub():


    def __init__(self, topics = None, type = 'subscriber'):
        self.client = None

        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

        self.type = type

        self.ADAFRUIT_IO_TOPICS_LIST = topics if topics is not None else None

    def read_config(self):
        fn = "./config/conf.json"

        with open(fn) as config_file:
            config_data = json.load(config_file)

            print("configuration file", fn, "read successful!")

            self.broker = config_data['adafruit']['broker']
            self.port = config_data['adafruit']['port']

            self.ADAFRUIT_IO_USERNAME = config_data['adafruit']['user']
            self.ADAFRUIT_IO_KEY = config_data['adafruit']['key']

            if self.ADAFRUIT_IO_TOPICS_LIST is None:
                self.ADAFRUIT_IO_TOPICS_LIST = config_data['adafruit']['topics']

            self.TRESH_TEMP_H = config_data['adafruit']['threshhold_temp_high']
            self.TRESH_TEMP_L = config_data['adafruit']['threshhold_temp_low']
            self.TRESH_HUM_H = config_data['adafruit']['threshhold_hum_high']
            self.TRESH_HUM_L = config_data['adafruit']['threshhold_hum_low']

    def read_data(self):
        try:
            ser = Serial('/dev/ttyACM1', baudrate=115200, timeout=1)
        except Exception as e:
                print("Error: ", e)
            
        time_old = 0
        while True:
            try:
                data_str = ser.readline().decode('ascii')
                if len(data_str) > 0:
                    data_dict = json.loads(data_str)
                    time_current = data_dict["time"]
                    if time_current > time_old:
                        time_old = time_current
                        self.temp = float(data_dict["temp"]) 
                        self.hum = float(data_dict["hum"]) 
                        self.dev_ID = data_dict["devID"]

                        if (-50.0 < self.temp < 100.0) and (0.0 < self.hum < 100.0): # check correct range
                            break
                            
                        else:
                            raise Exception('Werte Außerhalb des erlaubten Bereichs')

            except Exception as e:
                print("Error: " + str(e))


    def connect_mqtt(self):
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                
            else:
                print("Failed to connect, return code %d\n", rc)

        # Set Connecting Client ID
        client = mqtt_client.Client(self.client_id)
        client.username_pw_set(self.ADAFRUIT_IO_USERNAME, self.ADAFRUIT_IO_KEY)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)

        #
        self.client = client

        if self.type != 'subscriber':
            client.loop_start()
        

    def publish(self):
        #client.loop_start()
        if self.client is not None:
            if self.TRESH_TEMP_L < self.temp < self.TRESH_TEMP_H:
                topic_temp = self.ADAFRUIT_IO_TOPICS_LIST[0]
                msg_temp = f"{self.temp}"

            else:
                topic_temp = self.ADAFRUIT_IO_TOPICS_LIST[2]
                msg_temp = f"{self.temp}"

                

            if self.TRESH_HUM_L < self.hum < self.TRESH_HUM_H:
                topic_hum = self.ADAFRUIT_IO_TOPICS_LIST[1]
                msg_hum = f"{self.hum}"

            else:
                topic_hum = self.ADAFRUIT_IO_TOPICS_LIST[3]
                msg_hum = f"{self.hum}"
        else:
            print("client is none")

        for msg, topic in zip([msg_temp, msg_hum], [topic_temp, topic_hum]):
            result = self.client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")


    def subscribe(self, topics = None):
        def on_message(client, userdata, msg):

            now = datetime.now()
            current_time = now.strftime("%d.%m.%Y %H:%M:%S")

            if 'temp' in msg.topic:
                print(f"{current_time} - Temperatur:\t{msg.payload.decode()} C - Topic: '{msg.topic}'")

            elif 'hum' in msg.topic:
                print(f"{current_time} - Luftfeuchtigkeit:\t{msg.payload.decode()} % - Topic: '{msg.topic}'")

            else:
                print(f"{current_time} - Sensorwert:\t{msg.payload.decode()} - Topic: '{msg.topic}'")

        if topics is None:
            topics = self.ADAFRUIT_IO_TOPICS_LIST

        if self.client is not None:
            for topic in topics:
                self.client.subscribe(topic)
                self.client.on_message = on_message

            self.client.loop_forever()
        

    



