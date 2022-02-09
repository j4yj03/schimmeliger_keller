import MQTTSensorPubSub as pubsub


if __name__ == '__main__':


    topics = ["b_ilja/feeds/temperature", "b_ilja/feeds/humidity", "b_ilja/feeds/alarm-temp", "b_ilja/feeds/alarm-hum"]


    try:

        subscriber = pubsub.MQTTSensorPubSub(type = 'subscriber')

        subscriber.read_config()

        subscriber.connect_mqtt()
    

        while True:

            subscriber.subscribe(topics)
            
    except Exception as e:
        print(e)