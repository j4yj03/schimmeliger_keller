import time
import pycom
import json

from machine import Pin, deepsleep

#from dhtsensor import DHTSensor
#
#from mqttwrapper import MQTTWrapper

from dth import DTH

#from DHT11RinusW import DHT11

import globalvars


def run():

    #mqtt_client = MQTTWrapper(DEVICE_ID, ADA_USERNAME, ADA_KEY, ADA_TOPICS_LIST)

    dht_pin=Pin('P9', Pin.OPEN_DRAIN)	# connect DHT22 sensor data line to pin P9/G16 on the expansion board
    dht_pin(1)							# drive pin high to initiate data conversion on DHT sensor

    sensor_list = []

    for sensor_type, gpio_pin in zip(SENSOR_LIST, SENSOR_GPIO):

        pin = Pin(gpio_pin, mode=Pin.OPEN_DRAIN)

        dht_type = 0 if sensor_type == 'DHT11' else 1 if sensor_type == 'DHT22' else 0

        sensor = DTH(pin, dht_type)

        sensor_list.append(sensor)

    while True:

        data_to_publish = []

        try:

            for sensor in sensor_list:

                result = sensor.read()

                temp = result.temperature
                hum = result.humidity

                if sensor.sensortype() == 0:
                    temp_str = '{}.0'.format(temp)
                    hum_str = '{}.0'.format(hum)

                elif sensor.sensortype() == 1:
                    temp_str = '{:3.1f}'.format(temp / 1.0)
                    hum_str = '{:3.1f}'.format(hum / 1.0)

                else:
                    temp_str = 'invalid sensor'
                    hum_str = 'invalid sensor'


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

            deepsleep(SLEEP_TIMER_SEC * 1000)
            
        
        except Exception as e:
            print(e)

        

        
        #time.sleep(1)

            

        

##################################################################################################


 
pycom.heartbeat(False)
pycom.rgbled(0x1f0000)    # turn LED red

run()
