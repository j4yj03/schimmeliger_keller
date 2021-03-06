from machine import Pin, enable_irq, disable_irq
import time

class DHTSensor():
    '''
        Class to initialize and read a DHT11/DHT22 humidity/temperature sensor
        Based on: https://github.com/johnmcdnz/LoPy-DHT-transmission
        Modified by: Sidney Göhler
    '''


    def __init__(self, sensor_typ: str, gpio_pin: str):

        if sensor_typ in ["DHT11", "DHT22"] and 'P' in gpio_pin :
            self.sensor_typ = sensor_typ     
            self.dht_pin = Pin(gpio_pin, Pin.OPEN_DRAIN)	# connect DHT22/DHT11 sensor data line to pin P9/G16 on the expansion board
            self.dht_pin(1)							# drive pin high to initiate data conversion on DHT sensor
            print(self.dht_pin())
            self.temperature = 0
            self.humidity = 0
        else:
            raise Exception('Invalid sensortype or invalid Pin')

    # this onewire protocol code tested with Pycom LoPy device and AM2302/DHT22 sensor

    def _getval(self):

        if self.sensor_typ == 'DHT11':
            ms = [1]*1000   
        else:
            ms = [1]*700        # needs long sample size to grab all the bits from the DHT
        time.sleep(1)
        self.dht_pin(0)
        time.sleep_us(15000)
        self.dht_pin(1)
        irqf = disable_irq()
        for i in range(len(ms)):
            ms[i] = self.dht_pin()      ## sample input and store value

        enable_irq(irqf)
        #for i in range(len(ms)):		#print debug for checking raw data
        #    print (ms[i])
        self.input = ms

    def _decode(self):
        inp = self.input
        res = [0]*5
        self.bits=[]
        ix = 0
        try:
            if self.sensor_typ == 'DHT11':
                if inp[0] == 1: 
                    ix = inp.index(0, ix) ## skip to first 0	# ignore first '1' as probably sample of start signal.  *But* code seems to be missing the start signal, so jump this line to ensure response signal is identified in next two lines.
            ix = inp.index(1,ix) ## skip first 0's to next 1	#  ignore first '10' bits as probably the response signal.
            ix = inp.index(0,ix) ## skip first 1's to next 0
            while len(self.bits) < len(res)*8 : ##need 5 * 8 bits :
                ix = inp.index(1,ix) ## index of next 1
                ie = inp.index(0,ix) ## nr of 1's = ie-ix
                # print ('ie-ix:',ie-ix)
                self.bits.append(ie-ix)
                ix = ie
        except:
            print('6: decode error')
            print('length:')
            print(len(inp), len(self.bits))
            return([0xff, 0xff, 0xff, 0xff])

        print('bits:', self.bits)
        for i in range(len(res)):
            for v in self.bits[i * 8 : (i + 1) * 8]:   #process next 8 bit
                res[i] = res[i] << 1  ##shift byte one place to left
                if v > 5:                   #  less than 5 '1's is a zero, more than 5 1's in the sequence is a one
                    res[i] = res[i]+1  ##and add 1 if lsb is 1
                #print ('res',  i,  res[i])



        if (res[0] + res[1] + res[2] + res[3]) & 0xff != res[4] :
            #pass   ##parity error!
            print("Checksum Error:", (res[0] + res[1] + res[2] + res[3]) & 0xff, res)

            # res= [0xff,0xff,0xff,0xff]

        #print ('res:', res[0:4])
        return(res[0:4])
    
    def readSensor(self):

        self._getval()
        res = self._decode()

        print(self.dht_pin, self.input, res)

        if self.sensor_typ == 'DHT11':
            hum = 10  * res[0] + res[1]
            temp = 10 * res[2] + res[3]

        elif self.sensor_typ == 'DHT22':
            hum = res[0] * 256 + res[1]
            temp = res[2] * 256 + res[3]
            if (temp > 0x7fff):
                temp = 0x8000 - temp
        else:
            raise Exception('Uknown DHT Senortype')

        print(hum, temp)

        self.temperature = temp
        self.humidity = hum


    def getTemperature(self):
        if self.temperature != 0:
            return self.temperature
        else:
            return 0
            #raise Exception('Temperature not yet read')

    def getHumidity(self):
        if self.humidity != 0:
            return self.humidity
        else:
            return 0
            #raise Exception('Humidity not yet read')