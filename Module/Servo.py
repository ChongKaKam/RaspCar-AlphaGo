import time
import math
import smbus

# PCA9685 16-Channel PWM Servo Driver
# Author:   Chris
# Date:     2022-5-4

class Servo:
    def __init__(self,bus,address,on_L,on_H,off_L,off_H,correct=0) -> None:
        # register map
        self.bus = bus
        self.Address = address
        self.Register_ON_L  = on_L
        self.Register_ON_H  = on_H
        self.Register_OFF_L = off_L
        self.Register_OFF_H = off_H
        # attribution
        self.theta = 0
        self.pulse = 0
        self.correct = correct   # correct the theta

    def update(self, on, off):
        self.bus.write_byte_data(self.Address, self.Register_ON_L , on  & 0xFF)
        self.bus.write_byte_data(self.Address, self.Register_ON_H , on  >> 8)
        self.bus.write_byte_data(self.Address, self.Register_OFF_L, off & 0xFF)
        self.bus.write_byte_data(self.Address, self.Register_OFF_H, off >> 8)

    def SetAngle(self, theta):
        if theta>=0 and theta <= 180:
            self.theta = theta
            self.pulse = theta/180 * 2000 + 500 + self.correct
            k = self.pulse/20000
            pulse_data = int(4096*k)
            self.update(0, pulse_data)

    def SetPulse(self, pulse):
        # the PWM frequency is 50Hz (20000us)
        self.pulse = pulse
        
        self.theta = (pulse-500-self.correct)/2000*180
        k = pulse/20000
        pulse_data = int(4096*k)
        self.update(0, pulse_data)
        pass

    def Show(self, register_enable=False):
        if register_enable:
            print('Address:', self.Address)
            print('Register Map:')
            print('ON_L, ON_H', self.Register_ON_L, self.Register_ON_H)
            print('OFF_L, OFF_H', self.Register_OFF_L, self.Register_OFF_H)
        print('angle:', self.theta, 'pulse:', self.pulse)

class Servo_Manager:

    # PCA9685 Register Map
    __SUBADR1       = 0x02
    __SUBADR2       = 0x03
    __SUBADR3       = 0x04
    __MODE1         = 0x00          
    __PRESCALE      = 0xFE
    __LED0_ON_L     = 0x06
    __LED0_ON_H     = 0x07
    __LED0_OFF_L    = 0x08
    __LED0_OFF_H    = 0x09
    __LED1_ON_L     = 0x0A
    __LED1_ON_H     = 0x0B
    __LED1_OFF_L    = 0x0C
    __LED1_OFF_H    = 0x0D

    def __init__(self, address=0x40, PWMFreq=50) -> None:
        self.bus = smbus.SMBus(1)
        self.address = address
        self.PWMFreq = PWMFreq
        self.theta = [0,0]
        self.ServoX = Servo(self.bus, 
                            address, 
                            self.__LED0_ON_L, 
                            self.__LED0_ON_H,
                            self.__LED0_OFF_L,
                            self.__LED0_OFF_H,
                            200)
        self.ServoY = Servo(self.bus,
                            address,
                            self.__LED1_ON_L,
                            self.__LED1_ON_H,
                            self.__LED1_OFF_L,
                            self.__LED1_OFF_H,
                            0)
        self.bus.write_byte_data(self.address, self.__MODE1, 0x00)

    def SetPWMFreq(self, freq):
        "set the PWM frequency"
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1
        prescale = math.floor(prescaleval + 0.5)
        
        OLD_MODE = self.bus.read_byte_data(self.address, self.__MODE1)
        NEW_MODE = (OLD_MODE & 0x7F) | 0x10                             # set sleep cmd 
        self.bus.write_byte_data(self.address, self.__MODE1, NEW_MODE)  # sleep mode
        self.bus.write_byte_data(self.address, self.__PRESCALE, int(prescale))
        self.bus.write_byte_data(self.address, self.__MODE1, OLD_MODE)
        time.sleep(0.005)
        self.bus.write_byte_data(self.address, self.__MODE1, OLD_MODE | 0x80)

    def DeviceInit(self, thetaX=90, thetaY=30):
        self.SetPWMFreq(self.PWMFreq)
        time.sleep(0.001)
        self.SetTheta(thetaX, thetaY)

    def SetTheta(self, thetaX, thetaY):
        if thetaX<30 or thetaX>150: return
        if thetaY<0  or thetaY>60 : return
        self.ServoY.SetAngle(thetaY)
        self.ServoX.SetAngle(thetaX)
        self.theta = [thetaX, thetaY]
    
    def GetTheta(self):
        return self.theta

    def up(self, delta):
        self.SetTheta(self.theta[0], self.theta[1]-delta)

    def down(self, delta):
        self.SetTheta(self.theta[0], self.theta[1]+delta)

    def left(self, delta):
        self.SetTheta(self.theta[0]+delta, self.theta[1])

    def right(self, delta):
        self.SetTheta(self.theta[0]-delta, self.theta[1])


if __name__=="__main__":
    Manager = Servo_Manager()
    # Manager.SetPWMFreq(50)
    # Manager.ServoX.SetPulse(1600)
    # Manager.ServoX.SetAngle(60)
    # Manager.ServoY.SetAngle(0)
    Manager.DeviceInit()

    theta = Manager.GetTheta()
    print('[theta_X, theta_Y]:', theta)
    
