#!/usr/bin/python3

import json
import cv2
from datetime import datetime, timedelta
from tkinter import Tk, Frame, Label

from display.display import Display
from mqtt.mqtt import MqttClient
from camera.camera import CameraCapture

#------------------ Constants ------------------

FACE_OK_COLOR = (0, 255, 0)
FACE_ERROR_COLOR = (255, 0, 0)

SCREEN_WIDTH                   = 1024
SCREEN_HEIGHT                  = 600

# Topic
GPS_TOPIC                      = "local/sensor/gps"
RFID_TOPIC                     = "local/sensor/rfid"
FR_TOPIC                       = "local/face_recognize"
FACE_VERIFY_TOPIC              = "local/verify"

# Person
person1 = {"id" : 4182211, "name" : "Đỗ Hữu Thắng", "type" : "teacher", "last_s" : 0, "last_t": 0}
person2 = {"id" : 2682792, "name" : "Lại Thế Hoàng", "type" : "teacher", "last_s" : 0, "last_t": 0}
person3 = {"id" : 10477164, "name" : "Vũ Hồng Dương", "type" : "student", "last_s" : 2440, "last_t": 183600}
person4 = {"id" : 11025830, "name" : "Linh", "type" : "student", "last_s" : 1960, "last_t": 144060}

personList = [person1, person2, person3, person4]

#------------------ Manage ------------------

class Manage:
    def __init__(self):
        # Camera and display
        self.display = Display(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera = CameraCapture()
        self.mqttClient = MqttClient(self.parsingPacket)

        self.teacherId = -1
        self.studentId = -1
        self.teacherStart = datetime.now()
        self.teacherTime = 0
        self.teacherDistance = 0
        self.studentStart = datetime.now()
        self.studentTime = 0
        self.studentDistance = 0
        self.studentLastTime = timedelta(seconds = 0)
        self.studentLastDistance = 0

        # Face detection
        self.faceRecs = []
        self.showRecsCount = 0

        self.updateTime()
        self.updateCamera()

    #------------------ Parsing ------------------

    # Parsing data to info
    def parsingPacket(self, topic, packet):
        try:
            # Handle gps result
            if topic == GPS_TOPIC:
                gps = json.loads(packet)
                if(gps["command"] == "update"):
                    self.display.setLocation(str(gps["latitude"]), str(gps["longitude"]))

                    # Update distance
                    if self.teacherId > 0:
                        self.teacherDistance += gps["distance"]
                        self.display.setTeacherDistance(str(self.teacherDistance))
                    # Student
                    if self.studentId > 0:
                        self.studentDistance += gps["distance"]
                        self.studentLastDistance += gps["distance"]
                        # Display
                        self.display.setStudentDistance(str(self.studentDistance))
                        self.display.setStudentLastDistance(str(self.studentLastDistance))

            # Handle RFID result
            elif topic == RFID_TOPIC:
                rfid = json.loads(packet)
                if(rfid["command"] == "update"):
                    self.manageCheckInOut(rfid["card_id"])
            
            # Face recognition result
            elif topic == FR_TOPIC:
                self.showRecsCount = 0
                f_r = json.loads(packet)
                self.faceRecs = f_r["face_list"]

        except:
            print("error packet == " + packet)

    #------------------ Update ------------------

    # Update current time
    def updateTime(self):
        now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S") # Get current time
        self.display.setCurrentTime(now) # Show current time
        self.display.parent.after(1000, self.updateTime) # Call function after 1s
        
        # Update teacher time
        if self.teacherId > 0:
            time = datetime.now() - self.teacherStart
            self.display.setTeacherTime(str(time).split('.', 2)[0])

        # Update student time
        if self.studentId > 0:
            time = datetime.now() - self.studentStart
            self.studentLastTime += timedelta(seconds = 1)
            # Display
            self.display.setStudentTime(str(time).split('.', 2)[0])
            self.display.setStudentLastTime(str(self.studentLastTime))

    # Stream camera
    def updateCamera(self):
        # Get a frame from the video source
        ret, frame = self.camera.get_frame()

        if ret:
            # If face detected, show rectangles
            if len(self.faceRecs):
                for faceRec in self.faceRecs:
                    x1 = faceRec["left"]
                    y1 = faceRec["top"]
                    x2 = faceRec["right"]
                    y2 = faceRec["bottom"]
                    if faceRec["persion_id"] == 1:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), FACE_OK_COLOR, 2)
                    else:
                        cv2.rectangle(frame, (x1, y1), (x2, y2), FACE_ERROR_COLOR, 2)
            
            self.display.showCamera(frame)

        # Clear list after delay
        self.showRecsCount += 1
        if(self.showRecsCount > 5):
            self.faceRecs.clear()
        
        # Loop
        self.display.parent.after(10, self.updateCamera)

    #------------------ Check in/ out ------------------

    def clearTeacherInfo(self):
        self.teacherId = -1
        self.teacherStart = datetime.now()
        self.teacherDistance = 0
        # Display
        self.display.setTeacherName("")
        self.display.setTeacherStart("")
        self.display.setTeacherTime("")
        self.display.setTeacherDistance("")

    def clearStudentInfo(self):
        self.studentId = -1
        self.studentStart = datetime.now()
        self.studentDistance = 0
        # Display
        self.display.setStudentName("")
        self.display.setStudentStart("")
        self.display.setStudentTime("")
        self.display.setStudentDistance("")
        self.display.setStudentLastDistance("")
        self.display.setStudentLastTime("")

    def manageCheckInOut(self, card_id):
        for person in personList:
            if person["id"] == card_id:
                if person["type"] == "teacher":
                    # New or change teacher
                    if self.teacherId != card_id:
                        self.teacherId = card_id
                        self.teacherStart = datetime.now()
                        self.teacherDistance = 0
                        # Display
                        self.display.setTeacherName(person["name"])
                        self.display.setTeacherStart(self.teacherStart.strftime("%m/%d/%Y, %H:%M:%S"))
                        self.display.setTeacherTime("00:00:00")
                        self.display.setTeacherDistance("0")
                        self.display.setNotify("")

                    # Teacher checkout
                    else:
                        self.clearTeacherInfo()
                        self.clearStudentInfo()
                        break

                if person["type"] == "student":
                    # Teacher is checkout
                    if self.teacherId != -1:
                        # New or change student
                        if self.studentId != card_id:
                            self.studentId = card_id
                            self.studentStart = datetime.now()
                            self.studentDistance = 0
                            self.studentLastTime = timedelta(seconds = person["last_t"])
                            self.studentLastDistance = person["last_s"]

                            # Display
                            self.display.setStudentName(person["name"])
                            self.display.setStudentStart(self.studentStart.strftime("%m/%d/%Y, %H:%M:%S"))
                            self.display.setStudentTime("00:00:00")
                            self.display.setStudentDistance("0")
                            self.display.setStudentLastDistance(str(self.studentLastDistance))
                            self.display.setStudentLastTime(str(self.studentLastTime))
                            self.display.setNotify("")
                        
                        # Student checkout
                        else:
                            self.clearStudentInfo()

                    # Need a teacher before
                    else:
                        self.display.setNotify("Giảng viên cần check in trước")
                        break

                # Send to verify id
                data_set = {"command":"update", "card_list":[str(card_id)], "numbs_card":1}
                json_mess = json.dumps(data_set)
                self.mqttClient.publish(FACE_VERIFY_TOPIC, json_mess)
                break

#------------------ Run ------------------

# Main
manage = Manage()
manage.display.mainloop()         # Blocks