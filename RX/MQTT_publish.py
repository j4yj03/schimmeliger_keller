import json
from paho.mqtt import client as mqtt_client
import random

from serial import Serial




class Mqtt_sensor_publisher():

    def __init__(self):
        self.client = None
        self.broker = 'io.adafruit.com'
        self.port = 1883
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

    def read_config(self):
        fn = "./config/conf.json"

        with open(fn) as config_file:
            config_data = json.load(config_file)

            print("configuration file", fn, "read successful!")

            self.ADAFRUIT_IO_USERNAME = config_data['adafruit']['user']
            self.ADAFRUIT_IO_KEY = config_data['adafruit']['key']
            self.ADAFRUIT_IO_TOPICS_LIST = config_data['adafruit']['topics']

            self.TRESH_TEMP_H = config_data['adafruit']['threshhold_temp_high']
            self.TRESH_TEMP_L = config_data['adafruit']['threshhold_temp_low']
            self.TRESH_HUM_H = config_data['adafruit']['threshhold_hum_high']
            self.TRESH_HUM_L = config_data['adafruit']['threshhold_hum_low']

    def read_data(self):
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
                        
                        self.temp = data_dict["temp"] 
                        self.hum = data_dict["hum"] 
                        self.dev_ID = data_dict["devID"]

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

        client.loop_start()
        self.client = client

    def publish(self, topic, msg):
        if self.client is not None:

            if self.TRESH_TEMP_L < self.temp < self.TRESH_TEMP_H:
                topic = self.ADAFRUIT_IO_TOPICS_LIST[0]
                msg = f"{self.temp}"

            else:
                topic = self.ADAFRUIT_IO_TOPICS_LIST[2]
                msg = f"{self.temp}"

            if self.TRESH_HUM_L < self.hum < self.TRESH_HUM_H:
                topic = self.ADAFRUIT_IO_TOPICS_LIST[1]
                msg = f"{self.hum}"

            else:
                topic = self.ADAFRUIT_IO_TOPICS_LIST[3]
                msg = f"{self.hum}"


            msg = f"{msg}"
            result = self.client.publish(topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topic}`")
            else:
                print(f"Failed to send message to topic {topic}")
    
if __name__ == '__main__':

    try:

        publisher = Mqtt_sensor_publisher()

        publisher.read_config()

        publisher.connect_mqtt()
    

        while True:

            publisher.read_data()
            publisher.publish()
            
    except Exception as e:
        print(e)
    



