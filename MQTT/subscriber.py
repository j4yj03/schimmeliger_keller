import MQTTSensorPubSub as pubsub


if __name__ == '__main__':


    topics = ["b_ilja/feeds/temperature", "b_ilja/feeds/humidity", "b_ilja/feeds/alarm-temp", "b_ilja/feeds/alarm-hum"]


    try:

        publisher = pubsub.MQTTSensorPubSub(type = 'subscriber')

        publisher.read_config()

        publisher.connect_mqtt()
    

        while True:

            publisher.subscribe(topics)
            
    except Exception as e:
        print(e)