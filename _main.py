import time
from Module.Camera import CameraModule
from Module.RGB import LEDModule, Color

if __name__=="__main__":
    Camera = CameraModule()
    Camera.Servos.SetTheta(90,30)    
    theta = Camera.Servos.GetTheta()
    print(theta)
    LED = LEDModule()
    LED.setLED(0, Color(0,64,64))
    input('input any key to close')
    LED.close()
