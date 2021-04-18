#!/usr/bin/python3

from tkinter import Tk, Frame, Label, Canvas
from PIL import ImageTk, Image

#------------------ Constants ------------------

# Text font
TEXT_SMALL_SIZE                = 11
TEXT_LARGE_SIZE                = 14
TEXT_FONT                      = "Arial"

X0                             = 20
X1                             = 220
X2                             = 500
X3                             = 600

IMAGE_SIZE                     = 100

#------------------ Display ------------------

class Display:
    def __init__(self, width, height):
        self.parent = Tk()
        self.parent.title("Đào tạo lái xe")
        self.parent.geometry(str(width) + "x" + str(height)) # Set the geometry attribute to change the root windows size
        self.parent.resizable(0, 0) # Don't allow resizing in the x or y direction

        self.width = width
        self.height = height
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
        
        Label(self.parent, text = "Thời gian bắt đầu: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 100)
        self.teacherStartLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherStartLabel.place(x = X1, y = 100)
        
        Label(self.parent, text = "Thời gian: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 130)
        self.teacherTimeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherTimeLabel.place(x = X1, y = 130)

        Label(self.parent, text = "Quãng đường: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 160)
        self.teacherDistanceLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherDistanceLabel.place(x = X1, y = 160)

        # Student
        Label(self.parent, text = "Học viên: ", font = (TEXT_FONT, TEXT_LARGE_SIZE)).place(x = X0, y = 220)
        self.studentNameLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_LARGE_SIZE))
        self.studentNameLabel.place(x = X1, y = 220)
        
        Label(self.parent, text = "Thời gian bắt đầu: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 260)
        self.studentStartLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentStartLabel.place(x = X1, y = 260)

        Label(self.parent, text = "Tổng thời gian: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 290)
        self.studentTimeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentTimeLabel.place(x = X1, y = 290)

        Label(self.parent, text = "Quãng đường hiện tại: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 320)
        self.studentDistanceLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentDistanceLabel.place(x = X1, y = 320)

        Label(self.parent, text = "Quãng đường đã học: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 370)
        self.studentLastDistanceLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastDistanceLabel.place(x = X1, y = 370)

        Label(self.parent, text = "Thời gian đã học: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X0, y = 400)
        self.studentLastTimeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastTimeLabel.place(x = X1, y = 400)

        # Location
        Label(self.parent, text = "Vĩ độ: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X2, y = 370)
        self.latitudeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.latitudeLabel.place(x = X3, y = 370)

        Label(self.parent, text = "Kinh độ: ", font = (TEXT_FONT, TEXT_SMALL_SIZE)).place(x = X2, y = 400)
        self.longitudeLabel = Label(self.parent, text = "", font = (TEXT_FONT, TEXT_SMALL_SIZE))
        self.longitudeLabel.place(x = X3, y = 400)

        # Image
        image = Image.open("./image/default.png").resize((IMAGE_SIZE, IMAGE_SIZE))
        render = ImageTk.PhotoImage(image)
        self.teacherImage = Label(self.parent, image = render)
        self.teacherImage.image = render
        self.teacherImage.place(x = X2, y = 60)

        image = Image.open("./image/default.png").resize((IMAGE_SIZE, IMAGE_SIZE))
        render = ImageTk.PhotoImage(image)
        self.studentImage = Label(self.parent, image = render)
        self.studentImage.image = render
        self.studentImage.place(x = X2, y = 220)

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

    # Image
    def setTeacherImage(self, path):
        image = Image.open(path).resize((IMAGE_SIZE, IMAGE_SIZE))
        render = ImageTk.PhotoImage(image)
        self.teacherImage.configure(image = render)
        self.teacherImage.image = render

    def setStudentImage(self, path):
        image = Image.open(path).resize((IMAGE_SIZE, IMAGE_SIZE))
        render = ImageTk.PhotoImage(image)
        self.studentImage.configure(image = render)
        self.studentImage.image = render