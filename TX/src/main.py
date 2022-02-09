import time
# from TX.src.boot import SLEEP_TIMER_SEC
import pycom
import json
import struct

from machine import Pin, deepsleep, RTC

import globalvars

######################### BEGIN DEF RUN ########################################
def run():

    try:

        rtc = RTC()

        now = "".join(map(str, rtc.now()))

        from dth import DTH

        #dht_pin=Pin('P9', Pin.OPEN_DRAIN)	# connect DHT22 sensor data line to pin P9/G16 on the expansion board
        #dht_pin(1)							# drive pin high to initiate data conversion on DHT sensor

        sensor_list = []

        for sensor_type, gpio_pin, trans_driver_pin in zip(SENSOR_LIST, SENSOR_GPIO, SENSOR_TRANS_DRIVE):

            pin = Pin(gpio_pin, mode=Pin.OPEN_DRAIN)

            driver_pin = Pin(trans_driver_pin, mode=Pin.OUT, pull=Pin.PULL_DOWN)

            dht_type = 0 if sensor_type == 'DHT11' else 1 if sensor_type == 'DHT22' else 0

            sensor = DTH(pin, driver_pin, dht_type)

            sensor_list.append(sensor)
        

        for sensor in sensor_list:

            result = sensor.read()

            temp = result.temperature
            hum = result.humidity


            ####################################################### not needed (debug) #######
            '''
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
            '''
            #


            ##################################################################################

            condi = '(0 < '+ temp +'< 50.0) and (20.0 < '+ hum +' < 90.0)' if dht_type == 0 else '(-40.0 < '+ temp +' < 80.0) and (0.0 < '+ hum +' < 100.0)'
            

            if eval(condi): #DHT22 range
            
                format_str = 'QHffb'
                
                datatosend = struct.pack(format_str, int(now[0 : 14]), int(DEVICE_ID, 16), temp,  hum, sensor.sensortype())
                print("time:", int(now[0 : 14]), "DEV_ID:", int(DEVICE_ID, 16), "Temp:", temp,"Hum:", hum)
                
                import LoraMac_TX as lora

                lora.sendtoLoRa(datatosend)

            else:
                print('Sensor values out of range...')
    except Exception as e:
        print(e)


    finally:
        #print("sleeping for: " + str(SLEEP_TIMER_SEC) + " s")
        deepsleep(SLEEP_TIMER_SEC * 1000)
        

######################### END DEF RUN ########################################

pycom.heartbeat(False)

run()
