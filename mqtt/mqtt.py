#!/usr/bin/python3

import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, callback):
        self.mqttClient = mqtt.Client()
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
        self.callback = callback

        # Start mqtt client and subcribe to topic
        try:
            self.mqttClient.connect("52.191.248.141", 1883, 60)
            self.mqttClient.loop_start()
        except:
            print("Cannot connect to mqtt server")

    # The callback for when the client receives a CONNACK response from the server
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("#")

    # The callback for when a PUBLISH message is received from the server
    def on_message(self, client, userdata, msg):
        # print("topic == " + msg.topic + " message == " + msg.payload.decode("utf-8"))
        self.callback(msg.topic, msg.payload.decode("utf-8"))

    # Publish
    def publish(self, topic, message):
        self.mqttClient.publish(topic, message)