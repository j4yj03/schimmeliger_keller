from network import LoRa
import socket
import time
import pycom
import struct
import json

def LoraDemoRun():
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