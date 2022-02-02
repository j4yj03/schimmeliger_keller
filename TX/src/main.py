import time
import pycom
import json
import struct

from machine import Pin, deepsleep, RTC

import globalvars

######################### BEGIN DEF RUN ########################################
def run():

    try:

        rtc = machine.RTC()

        now = "".join(map(str, rtc.now()))

        from dth import DTH

        dht_pin=Pin('P9', Pin.OPEN_DRAIN)	# connect DHT22 sensor data line to pin P9/G16 on the expansion board
        dht_pin(1)							# drive pin high to initiate data conversion on DHT sensor

        sensor_list = []

        for sensor_type, gpio_pin in zip(SENSOR_LIST, SENSOR_GPIO):

            pin = Pin(gpio_pin, mode=Pin.OPEN_DRAIN)

            dht_type = 0 if sensor_type == 'DHT11' else 1 if sensor_type == 'DHT22' else 0

            sensor = DTH(pin, dht_type)

            sensor_list.append(sensor)
        

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

                

                print(now[0 : 14], data)

                datatosend = struct.pack('LHhH',int(now[0 : 14]), int(DEVICE_ID, 16), temp,  hum)

    
    except Exception as e:
        print(e)
        datatosend = struct.pack('LHhH',int(now[0 : 14]), int(DEVICE_ID, 16), str(e).encode(encoding = 'UTF-8'))

    try:

        import LoraMac_TX as lora

        lora.sendtoLoRa(datatosend)

    except Exception as e:
        print(e)

    finally:
        deepsleep(SLEEP_TIMER_SEC * 1000)

######################### END DEF RUN ########################################

pycom.heartbeat(False)

run()
