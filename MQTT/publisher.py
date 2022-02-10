import MQTTSensorPubSub as pubsub


if __name__ == '__main__':

    try:
        # publisher Objekt initialisieren
        publisher = pubsub.MQTTSensorPubSub(role = 'publisher', deviceSerialPort = '/dev/ttyACM1')

        # mit broker verbinden
        publisher.connect_mqtt()
    

        while True:
            # sensorwerte seriell auslesen
            publisher.read_data()
            # sensorwerte an broker übermitteln
            publisher.publish()
            
    except Exception as e:
        print(e)