try:
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

import sys
from PyQt5.QtWidgets import QApplication



class supportLibrary():

    def __init__(self):
        super().__init__()
    gpio_powerrelay = 7
    gpio_tfp3relay_pin = 3
    gpio_off = 0
    gpio_on = 1

    #******************************************************************************************
    def gpioInit(self):

        #example
        #GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  PUD_UP
        #GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
        #GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_tfp3relay_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(gpio_tfp3relay_pin, GPIO.OUT, initial=GPIO.LOW)
        gpio_on = 1
        gpio_off = 0

    #******************************************************************************************
    def getOsPlatform(self):
        platforms = {
            'linux1': 'Linux',
            'linux2': 'Linux',
            'darwin': 'OSX',
            'win32': 'Windows'
        }
        if sys.platform not in platforms:
            return sys.platform
        return platforms[sys.platform]



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = app()
    sys.exit(app.exec_())
