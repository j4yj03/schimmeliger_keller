import MQTTSensorPubSub as pubsub


if __name__ == '__main__':


    topicsList = ["b_ilja/feeds/temperature", "b_ilja/feeds/humidity", "b_ilja/feeds/alarm-temp", "b_ilja/feeds/alarm-hum"]


    try:
        # Subscriber Objekt erzeugen
        subscriber = pubsub.MQTTSensorPubSub(role = 'subscriber', topics = topicsList)

        # mit mqtt broker verbinden
        subscriber.connect_mqtt()
    
        while True:
            # am topic subscriben
            subscriber.subscribe()
            
    except Exception as e:
        print(e)