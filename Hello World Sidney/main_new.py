import time
import pycom
import binascii
import json

import dhtsensor as sensor
import machine

def load_config():
    try:

        with open("./config/conf.json") as config_file:
            config_data = json.load(config_file)

            return config_data

    except Exception as e:
        print(e)

def run():
    pass



run()