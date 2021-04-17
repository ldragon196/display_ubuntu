#!/usr/bin/python3

import re
import cv2
import json
import PIL.Image
import PIL.ImageTk
import paho.mqtt.client as mqtt

from tkinter import *
from datetime import datetime, timedelta

FACE_OK_COLOR = (0, 255, 0)
FACE_ERROR_COLOR = (255, 0, 0)

#------------------ Constants ------------------

DISPLAY_SIZE                   = "1024x600"
IMAGE_WIDTH                    = 440
IMAGE_HEIGHT                   = 440
IMAGE_X                        = 480
IMAGE_Y                        = 70

X_START                        = 20
X_CENTER                       = 512

TEXT_SMALL_SIZE                = 12
TEXT_LARGE_SIZE                = 16
TEXT_FONT                      = "Arial"

GPS_TOPIC                      = "local/sensor/gps"
RFID_TOPIC                     = "local/sensor/rfid"
FR_TOPIC                       = "local/sensor/face_recognize"

COLOR_RED                      = "#FF0000"

person1 = {"id" : 1234, "name" : "LongHD", "type" : "student", "last_s" : 2500, "last_t": timedelta(seconds = 14400) }
person2 = {"id" : 1235, "name" : "DuongHV", "type" : "student", "last_s" : 3500, "last_t": timedelta(seconds = 18000) }
person3 = {"id" : 1236, "name" : "TuongPV", "type" : "teacher", "last_s" : 0, "last_t": timedelta(seconds = 0) }
person4 = {"id" : 1237, "name" : "ThangDH", "type" : "teacher", "last_s" : 0, "last_t": timedelta(seconds = 0) }

personList = [person1, person2, person3, person4]

#--------------Get frame from camera----------

class CameraCapture:
    def __init__(self, camera_source=0):
        # Open the camera source
        self.vid = cv2.VideoCapture(camera_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open camera", camera_source)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            cv2.resize(frame, (IMAGE_WIDTH, IMAGE_HEIGHT))
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

#------------------ Display ------------------

class Display(Frame):
    def __init__(self, parent, camera_source=0):
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
        self.studentLastTime = 0
        self.studentLastDistance = 0
        self.initUI()

        # For face detection
        self.faceRecs = []
        self.faceCount = 0

        self.camera_source = camera_source
        # open camera source
        self.vid = CameraCapture(camera_source)
        # Create a canvas that can fit the above video source size
        # self.canvas = Canvas(parent, width = self.vid.width, height = self.vid.height)
        self.canvas = Canvas(parent, width = IMAGE_WIDTH, height = IMAGE_HEIGHT)
        self.canvas.place(x = IMAGE_X, y = IMAGE_Y)
        # self.canvas.pack()
        
        self.delay = 15
        self.update()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        if len(self.faceRecs):
            for faceRec in self.faceRecs:
                x1 = faceRec["x1"]
                y1 = faceRec["y1"]
                x2 = faceRec["x2"]
                y2 = faceRec["y2"]
                if faceRec["id"] == self.studentId:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), FACE_OK_COLOR, 1)
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), FACE_ERROR_COLOR, 1)
            # Clear list after delay
            self.faceCount += 1
            if(self.faceCount > 5):
                self.faceRecs.clear()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)

        self.parent.after(self.delay, self.update)

    # UI Initialization
    def initUI(self):
        # Current time
        self.currentTimeLabel = Label(window, text = "", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.currentTimeLabel.place(x = X_CENTER, y = 10, anchor="center")

        # Teacher
        self.teacherNameLabel = Label(self.parent, text = "Giảng viên: ", font=(TEXT_FONT, TEXT_LARGE_SIZE))         # Teacher name
        self.teacherNameLabel.place(x = X_START, y = 40)
        self.teacherStartLabel = Label(self.parent, text = "Thời gian bắt đầu: ", font=(TEXT_FONT, TEXT_SMALL_SIZE)) # Time checkin
        self.teacherStartLabel.place(x = X_START, y = 100)
        self.teacherTimeLabel = Label(self.parent, text = "Tổng thời gian: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))     # Time run
        self.teacherTimeLabel.place(x = X_START, y = 130)
        self.teacherDistanceLabel = Label(self.parent, text = "Quãng đường hiện tại: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherDistanceLabel.place(x = X_START, y = 160)

        # Student
        self.studentNameLabel = Label(self.parent, text = "Học viên: ", font=(TEXT_FONT, TEXT_LARGE_SIZE))
        self.studentNameLabel.place(x = X_START, y = 220)
        self.studentStartLabel = Label(self.parent, text = "Thời gian bắt đầu: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentStartLabel.place(x = X_START, y = 250)
        self.studentTimeLabel = Label(self.parent, text = "Tổng thời gian: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentTimeLabel.place(x = X_START, y = 280)
        self.studentDistanceLabel = Label(self.parent, text = "Quãng đường hiện tại: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentDistanceLabel.place(x = X_START, y = 310)
        self.studentLastDistanceLabel = Label(self.parent, text = "Quãng đường đã học: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastDistanceLabel.place(x = X_START, y = 340)
        self.studentLastTimeLabel = Label(self.parent, text = "Thời gian đã học: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastTimeLabel.place(x = X_START, y = 370)

        # Location
        self.latitudeLabel = Label(window, text = "Vĩ độ: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.latitudeLabel.place(x = X_START, y = 460)
        self.longitudeLabel = Label(window, text = "Kinh độ: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.longitudeLabel.place(x = X_START, y = 490)

        # Notify
        self.notifyLabel = Label(window, text = "", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.notifyLabel.place(x = X_CENTER, y = 560, anchor="center")
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
            display.studentLastTime += time
            self.setStudentTime(str(time))
            self.setStudentLastTime(str(display.studentLastTime))

    
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
                    display.studentLastDistance += display.studentDistance
                    # Display
                    display.setStudentDistance(str(display.studentDistance))
                    display.setStudentLastDistance(str(display.studentLastDistance))

        # Handle RFID result
        elif topic == RFID_TOPIC:
            rfid = json.loads(packet)
            if(rfid["command"] == "update"):
                manageCheckInOut(rfid["card_id"])
        
        # Face recognition result
        elif topic == FR_TOPIC:
            f_r = json.loads(packet)
            display.faceRecs = f_r["face_list"]
            

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
    display.setStudentLastDistance("")
    display.setStudentLastTime("")

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
                    display.setNotify("")

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
                        display.studentLastTime = person["last_t"]
                        display.studentLastDistance = person["last_s"]
                        display.setStudentLastDistance(str(person["last_s"]))
                        display.setStudentLastTime(str(person["last_t"]))
                        display.setNotify("")
                    
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
window.geometry(DISPLAY_SIZE) # Set the geometry attribute to change the root windows size
window.resizable(0, 0) # Don't allow resizing in the x or y direction

#------------------ Run ------------------
mqttInit()
display = Display(window, camera_source=0)
window.mainloop()



#------------------------------------ Command ------------------------------------
"""
topic: local/sensor/face_recognize
{
"command": "update",
"face_list": [
    {
        "id": 1,
        "x1": 20,
        "y1": 20,
        "x2": 40,
        "y2": 40
        },
        {
        "id": 2,
        "x1": 100,
        "y1": 100,
        "x2": 200,
        "y2": 200
        }
    ]
}

topic: local/sensor/gps
{
  "command":"update",
  "latitude":21.039755217646018, 
  "longitude":105.74732532739786,
  "distance":2.0123
}

topic: local/sensor/rfid
{
    "command":"update",
    "card_id": 123569874
}

topic: local/sensor/face_recognize
{
    "command": "update",
    "person_id": 1,
    "top": 0,
    "bottom": 180,
    "left": 0,
    "right": 180
}
"""