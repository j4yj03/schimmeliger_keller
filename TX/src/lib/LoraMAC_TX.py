from network import LoRa
import socket
import machine
import time
import pycom


#

# initialize LoRa in LORA mode
# more params can also be given, like frequency, tx power and spreading factor
print ("LoRa start...")
lora = LoRa(mode=LoRa.LORA,  frequency=868000000,  tx_power=20)

# create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

def sendtoLoRa(datatosend):

    print('LoRa send: {}\n'.format(datatosend))
    s.setblocking(True)
    s.send(datatosend)
    #s.send(dev_ID, str([temp]),  str([hum]))
    s.setblocking(False)

    
    


