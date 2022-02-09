import binascii
import json
import time
# pycom specific modules
import machine
from network import WLAN

import globalvars

def load_config():

    fn = "./config/conf.json"

    with open(fn) as config_file:
        config_data = json.load(config_file)

        print("configuration file",fn, "read successful!")

        return config_data


################################################################# not neeeded
'''
def connect_wifi():
    wlan = WLAN(mode=WLAN.STA, antenna=WLAN.EXT_ANT)
    nets = wlan.scan()
    for net in nets:
        if net.ssid == WIFI_SSID:
            max_tries = 3
            for ntry in range(max_tries):
                #print(wlan.isconnected(), wlan.ifconfig()[0])
                if not wlan.isconnected():
                    try:
                        wlan.connect(net.ssid, auth=(net.sec, WIFI_PASS), timeout=10000)
                        print('Connecting to:', net.ssid,"\nAttempt:", str(ntry + 1) + "/" + str(max_tries))

                        while not wlan.isconnected():
                            machine.idle() # Save power while waiting.
                    except Exception as e:
                        print('ERROR:', e)
                        time.sleep(5)
                else:
                    break
            

            print("Connected to", WIFI_SSID, wlan.ifconfig(), "\n")

'''
################################################################################

try:

    

    conf = load_config()

    SENSOR_LIST = conf['sensor']['sensortype']
    SENSOR_GPIO = conf['sensor']['gpiopin']
    SENSOR_TRANS_DRIVE = conf['sensor']['transdrivepin']


    DEVICE_ID = binascii.hexlify(machine.unique_id())

    SLEEP_TIMER_SEC = conf['machine']['sleeptimer_sec']

    print("Device ID:", DEVICE_ID, "\nSensor list:", SENSOR_LIST, "GPIO pins", SENSOR_GPIO, "Driver pins", SENSOR_TRANS_DRIVE)

    #connect_wifi()

except Exception as e:
    print(e)


