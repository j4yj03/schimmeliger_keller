import time
import pycom
import binascii
import json

from mqtt import MQTTClient
from network import WLAN

from machine import Pin
import machine
#from LoraMAC_TX import sendtoLoRa
#from DHT22RinusW import DHT22
from DHT11RinusW import DHT11



def load_config_data():
    config_file = open("config.json",)
    config_data = json.load(config_file)

    return config_data


def sub_cb(topic, msg):
   print(msg)


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


def mqtt_init(device_id, ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY):
    client = MQTTClient(device_id, "io.adafruit.com",user=ADAFRUIT_IO_USERNAME, password=ADAFRUIT_IO_KEY, port=1883)

    client.set_callback(sub_cb)
    client.connect()
    #client.subscribe(topic="youraccount/feeds/lights")

    return client

def mqtt_publish(mqtt_client, ADAFRUIT_IO_TOPIC, MESSAGE):
    mqtt_client.publish(topic=ADAFRUIT_IO_TOPIC, msg=MESSAGE)
    mqtt_client.check_msg()


def go_DHT(dev_ID):
    dht_pin=Pin('P9', Pin.OPEN_DRAIN)	# connect DHT22 sensor data line to pin P9/G16 on the expansion board
    dht_pin(1)							# drive pin high to initiate data conversion on DHT sensor
    
    while (True):
        temp, hum = DHT11(dht_pin)
        # temp = temp * 9 // 5 + 320   # uncomment for Fahrenheit
        temp_str = '{}.{}'.format(temp//10,temp%10)
        hum_str = '{}.{}'.format(hum//10,hum%10)
        # Print or upload it
        print('temp = {}C; hum = {}%'.format(temp_str, hum_str))

        if hum!=0xffff:
            #sendtoLoRa(dev_ID,  temp,  hum) #LoRa send

            data = json.dumps({
                    "temp" : temp_str,
                    "hum"  : hum_str
            })

            print(data)
            
            mqtt_publish(mqtt_client, data)

        time.sleep(10)

##################################################################################################


 
pycom.heartbeat(False)
pycom.rgbled(0x1f0000)    # turn LED red

conf = load_config_data()

WIFI_SSID = conf['wifi']['ssid']
WIFI_PASS = conf['wifi']['passpwd']

ADA_USERNAME = conf['adafruit']['user']
ADA_KEY = conf['adafruit']['key']
ADA_TOPICS_LIST = conf['adafruit']['topics']

device_ID = binascii.hexlify(machine.unique_id())


#f=open('device_name.py')   #get device name from file
#dev_ID = f.read()
print('Device ID:', device_ID[8:12])



connect_wifi(WIFI_SSID, WIFI_PASS)

mqtt_client = mqtt_init(device_ID)

go_DHT(device_ID[8:12])
