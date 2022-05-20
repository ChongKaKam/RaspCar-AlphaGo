# 
from pickle import FALSE
from Module.AlphaSocket import AlphaSocket
from Module.Camera import CameraModule
from Module.JoyStick import JoystickModule
from Module.Motor import MotorModule
from Module.RGB import LEDModule, Color
from Module.TRSensors import TRSensorModule

import threading
import time

# thread lock 
lock = threading.Lock()

# CmdDic = {
#     'forward': 1
# }

LED_RED = Color(64, 0, 0)
LED_GREEN = Color(0, 64, 0)
LED_WHITE = Color(64, 64, 64)

class AlphaSystem:
    def __init__(self) -> None:
        print(' AlphaGO v1.0 '.center(20,'-'))
        print('>> Init system devices...')
        print('>> Device Motor init...')
        self.Motor = MotorModule()
        print('>> Motor is ready.')
        print('>> Device LED init...')
        self.LED = LEDModule()
        self.led_state = False
        print('>> LED is ready.')
        print('>> Device JoyStick init...')
        self.JoyStick = JoystickModule()
        print('>> JoyStick is ready.')
        print('>> Device TRSensor init...')
        self.TR = TRSensorModule(5, self.Motor.avoid_object)
        self.tr_thread = threading.Thread(target=self.TR.detect_front)
        print('>> TRSensor is ready.')
        print('>> Device Camera init...')
        self.Camera = CameraModule()
        print('>> Camera is ready.')
        print('>> AlphaSocket init...')
        self.Socket = AlphaSocket(self.Camera.device,lock)
        print('>> AlphaSocket is  ready.')

    def Run(self):
        # RED means not ready
        self.LED.setAll(LED_RED)
        # self.LED.setLED(1,LED_GREEN)
        self.Socket.Control.start()
        self.tr_thread.start()
        while not self.Socket.Control.connection:
            pass
        motor_state = False
        delta = 2
        self.LED.setAll(LED_GREEN)
        while True:
            time.sleep(0.005)
            cmd = self.Socket.Control.getData()
            if cmd == None: continue
            if cmd == 'already quit': break
            print('cmd:', cmd)
            if cmd == 'w':
                # self.Camera.up(delta)
                if not self.TR.ifobject:
                    self.Motor.Forward()
                    # time.sleep(0.01)
                    # self.Motor.Stop()
            elif cmd == 's':
                # self.Camera.down(delta)
                self.Motor.Backward()
                # time.sleep(0.001)
            elif cmd == 'a':
                # self.Camera.left(delta)
                self.Motor.TurnLeft()
            elif cmd == 'd':
                # self.Camera.right(delta)
                self.Motor.TurnRight()
            elif cmd == 'stop':
                self.Motor.Stop()
            elif cmd == 'i':
                self.Camera.up(delta)
            elif cmd == 'k':
                self.Camera.down(delta)
            elif cmd == 'j':
                self.Camera.left(delta)
            elif cmd == 'l':
                self.Camera.right(delta)
            elif cmd == 'r':
                self.LED.setAll(LED_WHITE)
            elif cmd=='t':
                self.LED.close()
            elif cmd == 'v':
                if self.Socket.ifOpenVideo==False:
                    self.Socket.OpenVideo(str(self.Socket.Control.ip[0]))
            elif cmd == 'b':
                self.Socket.CloseVideo()
            elif cmd=='q':
                print('close TCP')
                break
        self.Socket.CloseVideo()
        self.Socket.CloseControl()
        self.TR.close_decte()
        if self.Socket.Video != None:
            if self.Socket.Video.is_alive():    
                self.Socket.Video.join()
        if self.tr_thread.is_alive():
            self.tr_thread.join()
        self.Socket.Control.join()
        

    def setLED(self):
        while self.led_state:
            self.LED.setLED(LED_WHITE)
            time.sleep(0.1)
        self.LED.close()
        
                
if __name__=="__main__":
    sys = AlphaSystem()
    sys.Run()
    sys.LED.close()