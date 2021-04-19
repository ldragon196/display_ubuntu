#!/usr/bin/python3

import cv2

class CameraCapture:
    def __init__(self, camera = 0):
        # Open the camera source
        self.vid = cv2.VideoCapture(camera)
        if not self.vid.isOpened():
            raise ValueError("Unable to open camera", camera)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
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
