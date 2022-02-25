import json
from network import WLAN

def load_config_data():
    config_file = open("/conf/config.json",)
    config_data = json.load(config_file)

    return config_data

def connect_wifi(WIFI_SSID, WIFI_PWD):
    wlan = WLAN(mode=WLAN.STA, antenna=WLAN.EXT_ANT)
    nets = wlan.scan()
    for net in nets:
        if net.ssid == WIFI_SSID:
            for i in range(3):
                try:
                    wlan.connect(net.ssid, auth=(net.sec, WIFI_PWD), timeout=10000)
                    break

                except Exception as e:
                    print('ERROR, Try again', i)
            #wlan.connect(SSID, auth=(WLAN.WPA2, PWD), timeout=5000)
            print('')
            while not wlan.isconnected():
                machine.idle() # Save power while waiting.

            print("Connected to", WIFI_SSID, wlan.ifconfig(), "\n")
            return wlan.isconnected()
            
            
conf = load_config_data()
            
WIFI_SSID = conf['wifi']['ssid']
WIFI_PASS = conf['wifi']['passpwd']

ADA_USERNAME = conf['adafruit']['user']
ADA_KEY = conf['adafruit']['key']
ADA_TOPICS_LIST = conf['adafruit']['topics']

WIFI_CONNECTED = connect_wifi(WIFI_SSID, WIFI_PASS)