import pycom
import time
import machine



mch = os.uname().machine
print(mch)


MOISTURE_SENSOR_PIN = 'P13'

adc = machine.ADC() #adc objekt

acd_pin = adc.channel(pin = MOISTURE_SENSOR_PIN) #adc pin definieren mit 6db attenuation#

while True:
    val = acd_pin() # Spannung messen
    print(val) # ausgeben

    time.sleep(1) # schlafen