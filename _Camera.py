import cv2 as cv
import threading

class CameraManager:
    def __init__(self,ServoManager) -> None:
        self.camera = cv.VideoCapture(0)
        if not self.camera.isOpened():
            print("ERR: Cannot open camera")
            return 1
        self.ServoManager = ServoManager

    def ShowVideo(self):
        # show vedio
        pass
    