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

        # systemzeit (tuple) als zeichenkette abspeichern (wird nach deepsleep nicht zurückgesetzt)
        now = "".join(map(str, rtc.now()))

        from dth import DTH

        # liste mit Sensoren initialisieren
        sensor_list = []

        for sensor_type, gpio_pin, trans_driver_pin in zip(SENSOR_LIST, SENSOR_GPIO, SENSOR_TRANS_DRIVE):

            # pin für Sensor initialisieren
            pin = Pin(gpio_pin, mode=Pin.OPEN_DRAIN)

            # pin für Transistoransteuerung definieren
            driver_pin = Pin(trans_driver_pin, mode=Pin.OUT, pull=Pin.PULL_DOWN)

            # dht Typ aus Wert in der configdatei bestimmen
            dht_type = 0 if sensor_type == 'DHT11' else 1 if sensor_type == 'DHT22' else 0

            # sensor Objekt erzeugen
            sensor = DTH(pin, driver_pin, dht_type)

            # in die Liste für Sensoren packen
            sensor_list.append(sensor)

        

        for sensor in sensor_list:

            # Sensor ansteuern, ecodieren und auslesen
            result = sensor.read()

            # Temperatur und Feuchtigkeitswerte aus dem Objekt auslesen
            temp = result.temperature
            hum = result.humidity

            # physikalische Grenzen definieren (aus Datenblatt)
            temp_h = 50.0 if sensor.sensortype() == 0 else 80.0
            temp_l = 0.0 if sensor.sensortype() == 0 else -40.0

            hum_h = 90.0 if sensor.sensortype() == 0 else 100.0
            hum_l = 20.0 if sensor.sensortype() == 0 else 0.0
            

            if (temp_l < temp < temp_h) and (hum_l < hum < hum_h): #check DHT11/22 range
            
                # byte format zur Datenübertragung definieren (u long long, u short, float, float, char)
                format_str = 'QHffb'
                
                # Daten in bytearray speichern
                datatosend = struct.pack(format_str, int(now[0 : 14]), int(DEVICE_ID, 16), temp,  hum, sensor.sensortype())
                #print("time:", int(now[0 : 14]), "DEV_ID:", int(DEVICE_ID, 16), "Temp:", temp,"Hum:", hum)
                
                # Lora Kommunikation initialisieren
                import LoraMac_TX as lora

                # LoRa Kommunikation starten
                lora.sendtoLoRa(datatosend)

            else:
                print('Sensor values out of range...')
    except Exception as e:
        print(e)


    finally:
        # deepsleep einleiten
        deepsleep(SLEEP_TIMER_SEC * 1000)
        

######################### END DEF RUN ########################################

pycom.heartbeat(False)

run()
