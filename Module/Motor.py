import RPi.GPIO as GPIO
import time

class MotorState:
    Stop = 0
    Forward = 1
    Backward = 2
    TurnLeft = 3
    TurnRight = 4

class MotorModule(object):
    
    def __init__(self, Ain1=12, Ain2=13, Aen=6, Bin1=20, Bin2=21, Ben=26) -> None:
        # default pin configuration
        self.AIN1 = Ain1
        self.AIN2 = Ain2
        self.BIN1 = Bin1
        self.BIN2 = Bin2
        self.ENA = Aen
        self.ENB = Ben
        # default speed (pwm duty)
        self.PA, self.PB = 50, 50
        # init GPIO and PWM
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.AIN1,GPIO.OUT)
        GPIO.setup(self.AIN2,GPIO.OUT)
        GPIO.setup(self.BIN1,GPIO.OUT)
        GPIO.setup(self.BIN2,GPIO.OUT)
        GPIO.setup(self.ENA,GPIO.OUT)
        GPIO.setup(self.ENB,GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)

        # init state
        self.state = MotorState.Stop
        self.Stop()
    
    def Stop(self):
        self.state = MotorState.Stop
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.LOW)
    
    def Forward(self):
        self.state = MotorState.Forward
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.HIGH)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.HIGH)

    def Backward(self):
        self.state = MotorState.Backward
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.AIN1,GPIO.HIGH)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.HIGH)
        GPIO.output(self.BIN2,GPIO.LOW)

    def TurnLeft(self):
        self.state = MotorState.TurnLeft
        self.PWMA.ChangeDutyCycle(30)
        self.PWMB.ChangeDutyCycle(30)
        GPIO.output(self.AIN1,GPIO.HIGH)
        GPIO.output(self.AIN2,GPIO.LOW)
        GPIO.output(self.BIN1,GPIO.LOW)
        GPIO.output(self.BIN2,GPIO.HIGH)

    def TurnRight(self):
        self.state = MotorState.TurnRight
        self.PWMA.ChangeDutyCycle(30)
        self.PWMB.ChangeDutyCycle(30)
        GPIO.output(self.AIN1,GPIO.LOW)
        GPIO.output(self.AIN2,GPIO.HIGH)
        GPIO.output(self.BIN1,GPIO.HIGH)
        GPIO.output(self.BIN2,GPIO.LOW)
    
    def SetSpeed(self, speed):
        if self.state != MotorState.Forward:
            return
        if speed >= 0 and speed <= 100:
            self.PWMA.ChangeDutyCycle(speed)
            self.PWMB.ChangeDutyCycle(speed)
            
if __name__=="__main__":
    AlphaGo = MotorModule()
    AlphaGo.TurnRight()
    try:
        while True:
            pass
    # speed = 50
    # flag = 1
    # try:
    #     while True:
    #         speed+=10*flag
    #         if speed==100: flag=-1
    #         if speed==0: flag=1
    #         AlphaGo.SetSpeed(speed)
    #         time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()