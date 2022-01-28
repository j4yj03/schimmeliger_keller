import time
import pycom

from dhtsensor import DHTSensor
from mqttwrapper import MQTTWrapper

import globalvars


def run():

    #mqtt_client = MQTTWrapper(DEVICE_ID, ADA_USERNAME, ADA_KEY, ADA_TOPICS_LIST)

    sensor_list = []

    for sensor_type, gpio_pin in zip(SENSOR_LIST, SENSOR_GPIO):

        sensor = DHTSensor(sensor_type, gpio_pin)

        sensor_list.append(sensor)

    while True:

        data_to_publish = []

        try:

            for sensor in sensor_list:
                sensor.readSensor()

                temp = sensor.getTemperature()
                hum = sensor.getHumidity()

                temp_str = '{}.{}'.format(temp//10, temp%10)
                hum_str = '{}.{}'.format(hum//10, hum%10)

                if (hum != 0xffff) and (temp != 0xffff):
                    
                    data = json.dumps({
                        "value": {"temp": float(temp_str), "hum": float(hum_str)},
                        "lat": 0.0,
                        "lon": 0.0,
                        "ele": 0
                    })

                    print(data)

                    data_to_publish.append(data)
                    
            #mqtt_client.publish(data_to_publish)
        
        except Exception as e:
            print(e)

        time.sleep(1)

            

        

##################################################################################################


 
pycom.heartbeat(False)
pycom.rgbled(0x1f0000)    # turn LED red

run()
