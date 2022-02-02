from mqtt import MQTTClient

class MQTTWrapper(MQTTClient):

    def __init__(self, device_id, user, key, topics):
        self.device_id = device_id
        self.user = user
        self.key = key
        self.topics = topics

        self.mqtt_client = super().__init__(self.device_id, "io.adafruit.com",user = self.user, password = self.key, port = 1883)
        self.set_callback(self.callback)
        self.mqtt_client = self.connect()


    def callback(self, msg):
        print(msg)


    def publish(self, MESSAGE_LIST):

        if not len(self.topics) == len(MESSAGE_LIST):
            raise Exception('MQTT Topics to Messages mismatch!', len(self.topics), "!=", len(MESSAGE_LIST))

        else:
            for MQTTtopic, MQTTmessage in zip(self.topics, MESSAGE_LIST):

                self.mqtt_client.publish(topic=MQTTtopic, msg=MQTTmessage)
                self.mqtt_client.check_msg()
