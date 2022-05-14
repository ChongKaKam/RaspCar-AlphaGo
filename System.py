# 
from Module.AlphaSocket import AlphaSocket
from Module.Camera import CameraModule
from Module.JoyStick import JoystickModule
from Module.Motor import MotorModule
from Module.RGB import LEDModule
from Module.TRSensors import TRSensorModule

class AlphaSystem:
    def __init__(self) -> None:
        print(' AlphaGO v1.0 '.center(20,'-'))
        print('>> Init system devices...')
        print('>> Device Motor init...')
        self.Motor = MotorModule()
        print('>> Motor is ready.')
        print('>> Device LED init...')
        self.LED = LEDModule()
        print('>> LED is ready.')
        print('>> Device JoyStick init...')
        self.JoyStick = JoystickModule()
        print('>> JoyStick is ready.')
        print('>> Device TRSensor init...')
        self.TR = TRSensorModule()
        print('>> TRSensor is ready.')
        print('>> Device Camera init...')
        self.Camera = CameraModule()
        print('>> Camera is ready.')
        print('>> AlphaSocket init...')
        self.Socket = AlphaSocket(self.Camera.device)
        print('>> AlphaSocket is  ready.')
        
    pass