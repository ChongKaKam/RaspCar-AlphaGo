import cv2
# from Servo import Servo_Manager
from Module.Servo import Servo_Manager


class CameraModule:
    def __init__(self, device=0) -> None:
        self.device = cv2.VideoCapture(device)
        if not self.device.isOpened(): 
            print('Cannot open camera')
            return None
        self.Servos = Servo_Manager()
        self.Servos.DeviceInit()

    def up(self, delta):
        self.Servos.up(delta)

    def down(self, delta):
        self.Servos.down(delta)

    def left(self, delta):
        self.Servos.left(delta)

    def right(self, delta):
        self.Servos.right(delta)
    

if __name__=="__main__":
    camera = CameraModule()
    