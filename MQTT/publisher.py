import MQTTSensorPubSub as pubsub


if __name__ == '__main__':

    try:

        publisher = pubsub.MQTTSensorPubSub()

        publisher.read_config()

        publisher.connect_mqtt()
    

        while True:

            publisher.read_data()
            publisher.publish()
            
    except Exception as e:
        print(e)