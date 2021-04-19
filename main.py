#!/usr/bin/python3

import json
from datetime import datetime, timedelta
from tkinter import Tk, Frame, Label

from display.display import Display
from mqtt.mqtt import MqttClient

#------------------ Constants ------------------

SCREEN_WIDTH                   = 1024
SCREEN_HEIGHT                  = 600

# Topic
GPS_TOPIC                      = "local/sensor/gps"
RFID_TOPIC                     = "local/sensor/rfid"
FR_TOPIC                       = "local/sensor/face_recognize"

# Image path
path1                          = "./image/Dominic_Toretto.png"
path2                          = "./image/Luke_Hobbs.png"
path3                          = "./image/Han_Lue.png"
path4                          = "./image/Gisele_Yashar.png"

# Person
person1 = {"id" : 4182211, "name" : "Dominic Toretto", "type" : "teacher", "last_s" : 0, "last_t": 0, "path":path1}
person2 = {"id" : 2682792, "name" : "Luke Hobbs", "type" : "teacher", "last_s" : 0, "last_t": 0, "path":path2}
person3 = {"id" : 10477164, "name" : "Han Lue", "type" : "student", "last_s" : 2440, "last_t": 183600, "path":path3}
person4 = {"id" : 11025830, "name" : "Gisele Yashar", "type" : "student", "last_s" : 1960, "last_t": 144060, "path":path4}

personList = [person1, person2, person3, person4]

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

#------------------ Update time ------------------

# Update current time
def updateTime():
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") # Get current time
    display.setCurrentTIme(now) # Show current time
    display.parent.after(1000, updateTime) # Call function after 1s

#------------------ Run ------------------

display = Display(SCREEN_WIDTH, SCREEN_HEIGHT)
updateTime()
mqttClient = MqttClient(parsingPacket)
display.mainloop()         # Blocks