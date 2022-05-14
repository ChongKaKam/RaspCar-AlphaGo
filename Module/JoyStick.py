import RPi.GPIO as GPIO
import time
from AlphaGo.Module.Servo import Servo_Manager

class Joystick:
    def __init__(self) -> None:
        self.CTR = 7
        self.A = 8
        self.B = 9
        self.C = 10
        self.D = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.CTR, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.A, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.B, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.C, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.D, GPIO.IN, GPIO.PUD_UP)
        
    def getkey(self):
        # key = [CTR, A, B, C, D]
        key = [0,0,0,0,0]
        key[0] = GPIO.input(self.CTR)
        key[1] = GPIO.input(self.A)
        key[2] = GPIO.input(self.B)
        key[3] = GPIO.input(self.C)
        key[4] = GPIO.input(self.D)
        return key
    
if __name__=="__main__":
    Stick = Joystick()
    ServoManager = Servo_Manager()
    theta_Y = 30
    theta_X = 90
    ServoManager.ServoY.SetAngle(theta_Y)
    ServoManager.ServoX.SetAngle(theta_X)
    # ServoManager.ServoX.SetPulse(7000)
    # ServoManager.ServoY.SetPulse(3000)
    delta = 0.5
    try:
        while True:
            key = Stick.getkey()
            if key[0] == 0:
                # CTR
                pass
            elif key[1] == 0:
                if theta_Y <= 60:
                    theta_Y += delta
                    ServoManager.ServoY.SetAngle(theta_Y)
            elif key[2] == 0:
                if theta_X >= 20:
                    theta_X -= delta
                    ServoManager.ServoX.SetAngle(theta_X)
            elif key[3] == 0:
                if theta_X <= 160:
                    theta_X += delta
                    ServoManager.ServoX.SetAngle(theta_X)
            elif key[4] == 0:
                if theta_Y >= 0:
                    theta_Y -= delta
                    ServoManager.ServoY.SetAngle(theta_Y)
                pass
            time.sleep(0.025/2)
    except KeyboardInterrupt:
        GPIO.cleanup()

