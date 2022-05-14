import time
from rpi_ws281x import PixelStrip, Color

class LEDModule:
    # LED strip configuration:
    LED_COUNT = 4        # Number of LED pixels.
    LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    def __init__(self) -> None:
        # create NeoPixel object with appropriate configuration.
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Initialize the lib (must be called once before other functions).
        self.strip.begin()
        # now you can operate your LEDs

    def close(self):
        print("clear data of LEDs")
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0,0,0))
            self.strip.show()
            time.sleep(50/1000.0)

    def numLED(self):
        return self.strip.numPixels()
    
    def setLED(self, seqLED, color, wait_ms=10):
        self.strip.setPixelColor(seqLED, color)
        self.strip.show()
        time.sleep(wait_ms/1000.0)
    
    def show(self):
        self.strip.show()

    def __del__(self):
        # clear DMA data
        self.close()

if __name__=="__main__":
    LEDs = LEDModule()
    num = LEDs.numLED()
    print('num:', num)
    try:
        while True:
            # R G B
            LEDs.setLED(0, Color(64,0,0))
            # print('0')
            LEDs.setLED(1, Color(0,64,0))
            # print('1')
            LEDs.setLED(2, Color(0,0,64))
            # print('2')
            LEDs.setLED(3, Color(64,64,0))
            # print('3')
            # LEDs.show()
            time.sleep(0.1)
    except KeyboardInterrupt:
        LEDs.close()
        pass
    
