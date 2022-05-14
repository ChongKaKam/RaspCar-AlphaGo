import cv2
from Servo import Servo_Manager


class CameraModule:
    def __init__(self, device=0) -> None:
        self.device = cv2.VideoCapture(device)
        if not self.device.isOpened(): 
            print('Cannot open camera')
            return None
        self.Servos = Servo_Manager()
        self.Servos.DeviceInit()
    

if __name__=="__main__":
    camera = CameraModule()
    