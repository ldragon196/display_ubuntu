import re
import json
from tkinter import *
from datetime import datetime
import paho.mqtt.client as mqtt

#------------------ Constants ------------------

TEXT_SMALL_SIZE                = 12
TEXT_LARGE_SIZE                = 16
TEXT_FONT                      = "Arial"

GPS_TOPIC                      = "local/sensor/gps"
RFID_TOPIC                     = "local/sensor/rfid"
FR_TOPIC                       = "local/sensor/face_recognize"

COLOR_RED                      = "#FF0000"

person1 = {"id" : 1234, "name" : "LongHD", "type" : "student", "last_s" : 2500, "last_t": 14400 }
person2 = {"id" : 1235, "name" : "DuongHV", "type" : "student", "last_s" : 3500, "last_t": 18000 }
person3 = {"id" : 1236, "name" : "TuongPV", "type" : "teacher", "last_s" : 0, "last_t": 0 }
person4 = {"id" : 1237, "name" : "ThangDH", "type" : "teacher", "last_s" : 0, "last_t": 0 }

personList = [person1, person2, person3, person4]

#------------------ Display ------------------

class Display(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.teacherId = -1
        self.studentId = -1
        self.teacherStart = datetime.now()
        self.teacherTime = 0
        self.teacherDistance = 0
        self.studentStart = datetime.now()
        self.studentTime = 0
        self.studentDistance = 0
        self.initUI()

    # UI Initialization
    def initUI(self):
        # Current time
        self.currentTimeLabel = Label(window, text = "", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.currentTimeLabel.place(x = 480, y = 10, anchor="center")

        # Teacher
        self.teacherNameLabel = Label(self.parent, text = "Giảng viên: ", font=(TEXT_FONT, TEXT_LARGE_SIZE))         # Teacher name
        self.teacherNameLabel.place(x = 40, y = 40)
        self.teacherStartLabel = Label(self.parent, text = "Thời gian bắt đầu: ", font=(TEXT_FONT, TEXT_SMALL_SIZE)) # Time checkin
        self.teacherStartLabel.place(x = 40, y = 100)
        self.teacherTimeLabel = Label(self.parent, text = "Tổng thời gian: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))     # Time run
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
        self.latitudeLabel.place(x = 340, y = 460, anchor="center")
        self.longitudeLabel = Label(window, text = "Kinh độ: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.longitudeLabel.place(x = 620, y = 460, anchor="center")

        # Notify
        self.notifyLabel = Label(window, text = "", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.notifyLabel.place(x = 480, y = 500, anchor="center")
        self.notifyLabel.configure(fg=COLOR_RED)

        # Update current time
        self.updateTime()


    # Update current time
    def updateTime(self):
        now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") # Get current time
        self.currentTimeLabel.configure(text = now) # Show current time
        self.parent.after(1000, self.updateTime) # Call function after 1s

        if self.teacherId > 0:
            time = datetime.now() - self.teacherStart
            self.setTeacherTime(str(time))

        if self.studentId > 0:
            time = datetime.now() - self.studentStart
            self.setStudentTime(str(time))

    
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

    # Notify
    def setNotify(self, notify):
        self.notifyLabel.configure(text = notify)
        
#------------------ Parsing ------------------

# Parsing data to info and show
def parsingPacket(topic, packet):
    try:
        # Handle gps result
        if topic == GPS_TOPIC:
            gps = json.loads(packet)
            if(gps["command"] == "update"):
                display.setLocation(str(gps["latitude"]), str(gps["longitude"]))
                # Update distance
                if display.teacherId > 0:
                    display.teacherDistance += gps["distance"]
                    display.setTeacherDistance(str(display.teacherDistance))
                if display.studentId > 0:
                    display.studentDistance += gps["distance"]
                    display.setStudentDistance(str(display.studentDistance))


        # Handle RFID result
        elif topic == RFID_TOPIC:
            rfid = json.loads(packet)
            if(rfid["command"] == "update"):
                manageCheckInOut(rfid["card_id"])
        
        # Face recognition result
        

    except:
        print("error packet == " + packet)

#------------------ Check in/ out ------------------

def clearTeacherInfo():
    display.teacherId = -1
    display.teacherStart = datetime.now()
    display.teacherDistance = 0
    display.setTeacherName("")
    display.setTeacherStart("")
    display.setTeacherTime("")
    display.setTeacherDistance("")

def clearStudentInfo():
    display.studentId = -1
    display.studentStart = datetime.now()
    display.studentDistance = 0
    display.setStudentName("")
    display.setStudentStart("")
    display.setStudentTime("")
    display.setStudentDistance("")

def manageCheckInOut(card_id):
    for person in personList:
        if person["id"] == card_id:
            if person["type"] == "teacher":
                # New or change teacher
                if display.teacherId != card_id:
                    display.teacherId = card_id
                    display.teacherStart = datetime.now()
                    display.teacherDistance = 0
                    display.setTeacherName(person["name"])
                    display.setTeacherStart(display.teacherStart.strftime("%m/%d/%Y, %H:%M:%S"))
                    display.setTeacherTime("00:00:00")
                    display.setTeacherDistance("0")

                # Teacher checkout
                else:
                    clearTeacherInfo()
                    clearStudentInfo()


            if person["type"] == "student":
                # Teacher is checkout
                if display.teacherId != -1:
                    # New or change student
                    if display.studentId != card_id:
                        display.studentId = card_id
                        display.studentStart = datetime.now()
                        display.studentDistance = 0
                        display.setStudentName(person["name"])
                        display.setStudentStart(display.studentStart.strftime("%m/%d/%Y, %H:%M:%S"))
                        display.setStudentTime("00:00:00")
                        display.setStudentDistance("0")
                        display.setStudentLastDistance(str(person["last_s"]))
                        display.setStudentLastTime(str(person["last_t"]))
                    
                    # Student checkout
                    else:
                        clearStudentInfo()

                # Need a teacher before
                else:
                    display.setNotify("Need a teacher before")

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

