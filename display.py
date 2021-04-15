import re
import json
from tkinter import *
import datetime
import paho.mqtt.client as mqtt

#------------------ Constants ------------------

TEXT_SMALL_SIZE                = 12
TEXT_LARGE_SIZE                = 16
TEXT_FONT                      = "Arial"

GPS_TOPIC                      = "local/sensor/gps"
RFID_TOPIC                     = "local/sensor/rfid"
FR_TOPIC                       = "local/sensor/face_recognize"

person1 = {"id" : 1234, "name" : "LongHD", "type" : "student" }
person2 = {"id" : 1235, "name" : "DuongHV", "type" : "student" }
person3 = {"id" : 1236, "name" : "TuongPV", "type" : "teacher" }
person4 = {"id" : 1237, "name" : "ThangDH", "type" : "teacher" }

personList = [person1, person2, person3, person4]

#------------------ Display ------------------

class Display(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.teacherId = -1
        self.studentId = -1
        self.teacherStart = 0
        self.teacherTime = 0
        self.teacherDistance = 0
        self.studentStart = 0
        self.studentTime = 0
        self.studentDistance = 0
        self.initUI()

    # UI Initialization
    def initUI(self):
        # Current time
        self.currentTimeLabel = Label(window, text = "", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.currentTimeLabel.place(x = 480, y = 10, anchor="center")

        # Teacher
        self.teacherNameLabel = Label(self.parent, text = "Giảng viên: ", font=(TEXT_FONT, TEXT_LARGE_SIZE))
        self.teacherNameLabel.place(x = 40, y = 40)
        self.teacherStartLabel = Label(self.parent, text = "Thời gian bắt đầu: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherStartLabel.place(x = 40, y = 100)
        self.teacherTimeLabel = Label(self.parent, text = "Tổng thời gian: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherTimeLabel.place(x = 520, y = 100)
        self.teacherDistanceLabel = Label(self.parent, text = "Quãng đường hiện tại: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherDistanceLabel.place(x = 40, y = 140)

        # Student
        self.studentNameLabel = Label(self.parent, text = "Học viên: ", font=(TEXT_FONT, TEXT_LARGE_SIZE))
        self.studentNameLabel.place(x = 40, y = 200)
        self.studentStartLabel = Label(self.parent, text = "Thời gian bắt đầu: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentStartLabel.place(x = 40, y = 260)
        self.studentTimeLabel = Label(self.parent, text = "Tổng thời gian: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentTimeLabel.place(x = 520, y = 260)
        self.studentDistanceLabel = Label(self.parent, text = "Quãng đường hiện tại: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentDistanceLabel.place(x = 40, y = 300)
        self.studentLastDistanceLabel = Label(self.parent, text = "Quãng đường đã học: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastDistanceLabel.place(x = 40, y = 340)
        self.studentLastTimeLabel = Label(self.parent, text = "Thời gian đã học: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastTimeLabel.place(x = 40, y = 380)

        # Location
        self.latitudeLabel = Label(window, text = "Vĩ độ: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.latitudeLabel.place(x = 340, y = 480, anchor="center")
        self.longitudeLabel = Label(window, text = "Kinh độ: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.longitudeLabel.place(x = 620, y = 480, anchor="center")

        # Update current time
        self.updateTime()


    # Update current time
    def updateTime(self):
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") # Get current time
        self.currentTimeLabel.configure(text = now) # Show current time
        self.parent.after(1000, self.updateTime) # Call function after 1s

    # Teacher
    def setTeacherName(self, name):
        self.teacherNameLabel.configure(text = "Giảng viên: " + name)

    def setTeacherStart(self, start):
        self.teacherStartLabel.configure(text = "Thời gian bắt đầu: " + start)

    def setTeacherTime(self, time):
        self.teacherTimeLabel.configure(text = "Tổng thời gian: " + time)

    def setTeacherDistance(self, distance):
        self.teacherDistanceLabel.configure(text = "Quãng đường hiện tại: " + distance)
    
    # Student
    def setStudentName(self, name):
        self.studentDistanceLabel.configure(text = "Học viên: " + name)

    def setStudentStart(self, start):
        self.studentStartLabel.configure(text = "Thời gian bắt đầu: " + start)

    def setStudentTime(self, time):
        self.studentTimeLabel.configure(text = "Tổng thời gian: " + time)

    def setStudentDistance(self, distance):
        self.studentDistanceLabel.configure(text = "Quãng đường hiện tại: " + distance)

    def setStudentLastDistance(self, last):
        self.studentLastDistanceLabel.configure(text = "Quãng đường đã học: " + last)
    
    def setStudentLastTime(self, last):
        self.studentLastTimeLabel.configure(text = "Thời gian đã học: " + last)
        
    # Location
    def setLocation(self, lat, lng):
        self.latitudeLabel.configure(text = "Vĩ độ: " + lat)
        self.longitudeLabel.configure(text = "Kinh độ: " + lng)
        
#------------------ Parsing ------------------

# Parsing data to info and show
def parsingPacket(topic, packet):
    try:
        # Handle gps result
        if topic == GPS_TOPIC:
            gps = json.loads(packet)
            if(gps["command"] == "update"):
                display.setLocation(str(gps["latitude"]), str(gps["longitude"]))
                print(gps["distance"])

        # Handle RFID result
        elif topic == RFID_TOPIC:
            rfid = json.loads(packet)
            if(rfid["command"] == "update"):
                manageCheckInOut(rfid["card_id"])
        
        # Face recognition result


    except:
        print("error packet == " + packet)

#------------------ Check in/ out ------------------

def manageCheckInOut(card_id):
    for person in personList:
        if person["id"] == card_id:
            if person["type"] == "teacher":
                # New or change teacher
                if display.teacherId != card_id:
                    display.setTeacherName(person["name"])



            if person["type"] == "student":
                # New or change student
                if display.teacherId != -1:
                    display.setStudentStart(person["name"])

#------------------ MQTT ------------------

# The callback for when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    # print("topic == " + msg.topic + " message == " + msg.payload.decode("utf-8"))
    parsingPacket(msg.topic, msg.payload.decode("utf-8"))

# Mqtt client intialization
mqtt_client = mqtt.Client()
def mqttInit():
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Start mqtt client and subcribe to topic
    try:
        mqtt_client.connect("52.191.248.141", 1883, 60)
        mqtt_client.loop_start()
    except:
        print("Cannot connect to mqtt server")

#------------------ Main GUI ------------------

window = Tk()
window.title("Đào tạo lái xe")
window.geometry("960x540") # Set the geometry attribute to change the root windows size
window.resizable(0, 0) # Don't allow resizing in the x or y direction

#------------------ Run ------------------
mqttInit()
display = Display(window)
window.mainloop()

