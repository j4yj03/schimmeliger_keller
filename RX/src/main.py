### LoRa-Empfänger 
### Code entnommen von https://github.com/johnmcdnz/LoPy-DHT-transmission/

from mqtt import MQTTClient

from network import LoRa
import socket
import time
import pycom
import struct
import json

import globalvars

def LoraReceive():
    #set to have no heart beat
    pycom.heartbeat(False)
    # initialize LoRa in LORA mode
    lora = LoRa(mode=LoRa.LORA, frequency=868000000)
    # create a raw LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    print("Started")
    while True:        
        time.sleep(1)
        data_raw = s.recv(64)
        #if Data has been received
        if data_raw != b'':
            uData = struct.unpack("QHffb",  data_raw)
            uData_json = json.dumps({
                "time":uData[0],
                "devID":uData[1],
                "temp":'{}.0'.format(uData[2]) if uData[4] == 0 else '{:3.1f}'.format(uData[2] / 1.0),
                "hum":'{}.0'.format(uData[3]) if uData[4] == 0 else '{:3.1f}'.format(uData[3] / 1.0)
            })
            print(uData_json)
            #print ( '{}.{}'.format(uData[0]))
            pycom.rgbled(0x007f00) # green
            time.sleep(1)
            pycom.rgbled(0x000000) # off


def mqtt_init(device_id, ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY):
    client = MQTTClient(device_id, "io.adafruit.com",user=ADAFRUIT_IO_USERNAME, password=ADAFRUIT_IO_KEY, port=1883)

    client.set_callback(sub_cb)
    client.connect()
    #client.subscribe(topic="youraccount/feeds/lights")

    return client

def mqtt_publish(mqtt_client, ADAFRUIT_IO_TOPIC, MESSAGE):
    mqtt_client.publish(topic=ADAFRUIT_IO_TOPIC, msg=MESSAGE)
    mqtt_client.check_msg()

def sub_cb(topic, msg):
   print(msg)
   
mqtt_client = mqtt_init(device_ID)

LoraReceive()




