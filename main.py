#!/usr/bin/python3

import json
from tkinter import Tk, Frame, Label
from display.display import Display
from mqtt.mqtt import MqttClient

#------------------ Constants ------------------

SCREEN_WIDTH                   = 800
SCREEN_HEIGHT                  = 450

# Topic
GPS_TOPIC                      = "local/sensor/gps"
RFID_TOPIC                     = "local/sensor/rfid"
FR_TOPIC                       = "local/sensor/face_recognize"

#------------------ Parsing ------------------

# Parsing data to info
def parsingPacket(topic, packet):
    try:
        # Handle gps result
        if topic == GPS_TOPIC:
            gps = json.loads(packet)
            if(gps["command"] == "update"):
                display.setLocation(str(gps["latitude"]), str(gps["longitude"]))

        # Handle RFID result
        elif topic == RFID_TOPIC:
            rfid = json.loads(packet)
            if(rfid["command"] == "update"):
                print(rfid["card_id"])
        
        # Face recognition result
        

    except:
        print("error packet == " + packet)

#------------------ Run ------------------

display = Display(SCREEN_WIDTH, SCREEN_HEIGHT)
mqttClient = MqttClient(parsingPacket)
display.mainloop()         # Blocks