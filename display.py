import re
import json
from tkinter import *
import datetime
import paho.mqtt.client as mqtt

#------------------ Constants ------------------

TEXT_SMALL_SIZE                = 12
TEXT_LARGE_SIZE                = 16
TEXT_FONT                      = "Arial"

#------------------ Manage ------------------

class Manage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    # UI Initialization
    def initUI(self):
        # Current time
        self.currentTimeLabel = Label(window, text = "", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.currentTimeLabel.place(x = 480, y = 10, anchor="center")

        # Teacher
        self.setTeacherName("")
        self.setTeacherStart("")
        self.setTeacherTime("")
        self.setTeacherDistance("")

        # Student
        self.setStudentName("")
        self.setStudentStart("")
        self.setStudentTime("")
        self.setStudentDistance("")
        self.setStudentLastDistance("")
        self.setStudentLastTime("")

        # Location
        self.setLocation("", "")

        # Update current time
        self.updateTime()


    # Update current time
    def updateTime(self):
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") # Get current time
        self.currentTimeLabel.configure(text = now) # Show current time
        self.parent.after(1000, self.updateTime) # Call function after 1s

    # Teacher
    def setTeacherName(self, name):
        teacherNameLabel = Label(self.parent, text = "Giảng viên: " + name, font=(TEXT_FONT, TEXT_LARGE_SIZE))
        teacherNameLabel.place(x = 40, y = 40)

    def setTeacherStart(self, start):
        teacherStartLabel = Label(self.parent, text = "Thời gian bắt đầu: " + start, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        teacherStartLabel.place(x = 40, y = 100)

    def setTeacherTime(self, time):
        teacherTimeLabel = Label(self.parent, text = "Tổng thời gian: " + time, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        teacherTimeLabel.place(x = 520, y = 100)

    def setTeacherDistance(self, distance):
        teacherDistanceLabel = Label(self.parent, text = "Quãng đường hiện tại: " + distance, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        teacherDistanceLabel.place(x = 40, y = 140)
    
    # Student
    def setStudentName(self, name):
        studentNameLabel = Label(self.parent, text = "Học viên: " + name, font=(TEXT_FONT, TEXT_LARGE_SIZE))
        studentNameLabel.place(x = 40, y = 200)

    def setStudentStart(self, start):
        studentStartLabel = Label(self.parent, text = "Thời gian bắt đầu: " + start, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        studentStartLabel.place(x = 40, y = 260)

    def setStudentTime(self, time):
        studentTimeLabel = Label(self.parent, text = "Tổng thời gian: " + time, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        studentTimeLabel.place(x = 520, y = 260)

    def setStudentDistance(self, distance):
        studentDistanceLabel = Label(self.parent, text = "Quãng đường hiện tại: " + distance, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        studentDistanceLabel.place(x = 40, y = 300)

    def setStudentLastDistance(self, last):
        studentLastDistanceLabel = Label(self.parent, text = "Quãng đường đã học: " + last, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        studentLastDistanceLabel.place(x = 40, y = 340)
    
    def setStudentLastTime(self, last):
        studentLastTimeLabel = Label(self.parent, text = "Thời gian đã học: " + last, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        studentLastTimeLabel.place(x = 40, y = 380)
        
    # Location
    def setLocation(self, lat, lng):
        latitudeLabel = Label(window, text = "Vĩ độ: " + lat, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        latitudeLabel.place(x = 360, y = 500, anchor="center")
        longitudeLabel = Label(window, text = "Kinh độ: " + lng, font=(TEXT_FONT, TEXT_SMALL_SIZE))
        longitudeLabel.place(x = 600, y = 500, anchor="center")
        
#------------------ MQTT ------------------

# Parsing data to info and show
def parsing_packet(packet):
    manage.setTeacherName(packet)

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    print("topic === " + msg.topic + " message == " + msg.payload.decode("utf-8"))
    parsing_packet(msg.payload.decode("utf-8"))

# Mqtt client intialization
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Start mqtt client and subcribe to topic
mqtt_client.connect("52.191.248.141", 1883, 60)
mqtt_client.loop_start()

#------------------ Main GUI ------------------

window = Tk()
window.title("Đào tạo lái xe")
window.geometry("960x540") # Set the geometry attribute to change the root windows size
window.resizable(0, 0) # Don't allow resizing in the x or y direction

#------------------ Run ------------------
manage = Manage(window)
window.mainloop()

