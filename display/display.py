#!/usr/bin/python3

from tkinter import Tk, Frame, Label, Canvas
from PIL import ImageTk, Image

from camera.camera import CameraCapture

#------------------ Constants ------------------

# Text font
TEXT_SMALL_SIZE                = 12
TEXT_LARGE_SIZE                = 14
TEXT_FONT                      = "Arial"

X0                             = 40
X1                             = 220

IMAGE_WIDTH                    = 480
IMAGE_HEIGHT                   = 360

COLOR_RED                      = "#FF0000"

#------------------ Display ------------------

class Display:
    def __init__(self, width, height):
        self.parent = Tk()
        self.parent.title("Đào tạo lái xe")
        self.parent.geometry(str(width) + "x" + str(height)) # Set the geometry attribute to change the root windows size
        self.parent.resizable(0, 0) # Don't allow resizing in the x or y direction

        self.width = width
        self.height = height
        self.cameraVideo = CameraCapture()
        self.initUI()
    
    def mainloop(self):
        self.parent.mainloop()

    # UI Initialization
    def initUI(self):
        # Current time
        self.currentTimeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.currentTimeLabel.place(x = self.width / 2, y = 20, anchor = "center")
        
        # Teacher
        Label(self.parent, text = "Giảng viên: ", font = (TEXT_FONT, TEXT_LARGE_SIZE)).place(x = X0, y = 60)
        self.teacherNameLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_LARGE_SIZE))
        self.teacherNameLabel.place(x = X1, y = 60)
        
        Label(self.parent, text = "Thời gian bắt đầu: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 120)
        self.teacherStartLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherStartLabel.place(x = X1, y = 120)
        
        Label(self.parent, text = "Thời gian: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 150)
        self.teacherTimeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherTimeLabel.place(x = X1, y = 150)

        Label(self.parent, text = "Quãng đường: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 180)
        self.teacherDistanceLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherDistanceLabel.place(x = X1, y = 180)

        # Student
        Label(self.parent, text = "Học viên: ", font = (TEXT_FONT, TEXT_LARGE_SIZE)).place(x = X0, y = 240)
        self.studentNameLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_LARGE_SIZE))
        self.studentNameLabel.place(x = X1, y = 240)
        
        Label(self.parent, text = "Thời gian bắt đầu: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 280)
        self.studentStartLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentStartLabel.place(x = X1, y = 280)

        Label(self.parent, text = "Tổng thời gian: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 310)
        self.studentTimeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentTimeLabel.place(x = X1, y = 310)

        Label(self.parent, text = "Quãng đường hiện tại: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 340)
        self.studentDistanceLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentDistanceLabel.place(x = X1, y = 340)

        Label(self.parent, text = "Quãng đường đã học: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 380)
        self.studentLastDistanceLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastDistanceLabel.place(x = X1, y = 380)

        Label(self.parent, text = "Thời gian đã học: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 410)
        self.studentLastTimeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastTimeLabel.place(x = X1, y = 410)

        # Location
        self.latitudeLabel = Label(self.parent, text = "Vĩ độ: ", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.latitudeLabel.place(x = 340, y = 480, anchor = "center")
        self.longitudeLabel = Label(self.parent, text = "Kinh độ: ", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.longitudeLabel.place(x = 680, y = 480, anchor = "center")

        # Image
        image = Image.open("./image/default.png").resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        render = ImageTk.PhotoImage(image)
        self.teacherImage = Label(self.parent, image = render)
        self.teacherImage.image = render
        self.teacherImage.place(x = 500, y = 60)
        self.updateCamera()

        # Notify
        self.notifyLabel = Label(self.parent, text = "basldasldna;d", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.notifyLabel.place(x = 512, y = 540, anchor = "center")
        self.notifyLabel.configure(fg = COLOR_RED)

    # Update current time
    def setCurrentTIme(self, time):
        self.currentTimeLabel.configure(text = time)

    # Teacher
    def setTeacherName(self, name):
        self.teacherNameLabel.configure(text = name)

    def setTeacherStart(self, start):
        self.teacherStartLabel.configure(text = start)

    def setTeacherTime(self, time):
        self.teacherTimeLabel.configure(text = time)

    def setTeacherDistance(self, distance):
        self.teacherDistanceLabel.configure(text = distance)
    
    # Student
    def setStudentName(self, name):
        self.studentDistanceLabel.configure(text = name)

    def setStudentStart(self, start):
        self.studentStartLabel.configure(text = start)

    def setStudentTime(self, time):
        self.studentTimeLabel.configure(text = time)

    def setStudentDistance(self, distance):
        self.studentDistanceLabel.configure(text = distance)

    def setStudentLastDistance(self, last):
        self.studentLastDistanceLabel.configure(text = last)
    
    def setStudentLastTime(self, last):
        self.studentLastTimeLabel.configure(text = last)

    # Location
    def setLocation(self, lat, lng):
        self.latitudeLabel.configure(text = lat)
        self.longitudeLabel.configure(text = lng)

    # Notify
    def setNotify(self, notify):
        self.notifyLabel.configure(text = notify)

    # Image
    def updateCamera(self):
        # Get a frame from the video source
        ret, frame = self.cameraVideo.get_frame()

        if ret:
            image = Image.fromarray(frame).resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            render = ImageTk.PhotoImage(image)
            self.teacherImage.configure(image = render)
            self.teacherImage.image = render

        self.parent.after(15, self.updateCamera)