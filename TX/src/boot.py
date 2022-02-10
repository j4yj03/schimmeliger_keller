import binascii
import json
# pycom specific modules
import machine

import globalvars

def load_config():

    fn = "./config/conf.json"

    with open(fn) as config_file:
        config_data = json.load(config_file)

        print("configuration file",fn,"read successful!")

        return config_data


try:

    conf = load_config()

    SENSOR_LIST = conf['sensor']['sensortype']
    SENSOR_GPIO = conf['sensor']['gpiopin']
    SENSOR_TRANS_DRIVE = conf['sensor']['transdrivepin']

    DEVICE_ID = binascii.hexlify(machine.unique_id())

    SLEEP_TIMER_SEC = conf['machine']['sleeptimer_sec']

    print("Device ID:", DEVICE_ID, "\nSensor list:", SENSOR_LIST, "GPIO pins", SENSOR_GPIO, "Driver pins", SENSOR_TRANS_DRIVE)

except Exception as e:
    print(e)


