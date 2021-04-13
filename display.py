import re
from tkinter import *
import datetime

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
        self.teacherName = Label(self.parent, text = "Giảng viên: ", font=(TEXT_FONT, TEXT_LARGE_SIZE))
        self.teacherName.place(x = 40, y = 40)
        self.teacherStart = Label(self.parent, text = "Thời gian bắt đầu: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherStart.place(x = 40, y = 100)
        self.teacherTime = Label(self.parent, text = "Tổng thời gian: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherTime.place(x = 520, y = 100)
        self.teacherDistance = Label(self.parent, text = "Quãng đường hiện tại: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.teacherDistance.place(x = 40, y = 140)

        # Student
        self.studentName = Label(self.parent, text = "Học viên: ", font=(TEXT_FONT, TEXT_LARGE_SIZE))
        self.studentName.place(x = 40, y = 200)
        self.studentStart = Label(self.parent, text = "Thời gian bắt đầu: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentStart.place(x = 40, y = 260)
        self.studentTime = Label(self.parent, text = "Tổng thời gian: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentTime.place(x = 520, y = 260)
        self.studentDistance = Label(self.parent, text = "Quãng đường hiện tại: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentDistance.place(x = 40, y = 300)
        self.studentLastDistance = Label(self.parent, text = "Quãng đường đã học: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastDistance.place(x = 40, y = 340)
        self.studentLastTime = Label(self.parent, text = "Thời gian đã học: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.studentLastTime.place(x = 40, y = 380)

        # Location
        self.latitude = Label(window, text = "Vĩ độ: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.latitude.place(x = 360, y = 500, anchor="center")
        self.longitude = Label(window, text = "Kinh độ: ", font=(TEXT_FONT, TEXT_SMALL_SIZE))
        self.longitude.place(x = 600, y = 500, anchor="center")

        self.updateInfo()


    # Update info
    def updateInfo(self):
        now = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") # Get current time
        self.currentTimeLabel.configure(text = now) # Show current time

        
        self.parent.after(1000, self.updateInfo) # Call function after 1s


#------------------ Main GUI ------------------
window = Tk()
window.title("Đào tạo lái xe")
window.geometry("960x540") # Set the geometry attribute to change the root windows size
window.resizable(0, 0) # Don't allow resizing in the x or y direction

#------------------ Run ------------------
manage = Manage(window)
window.mainloop()

