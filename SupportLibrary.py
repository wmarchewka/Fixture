# used to get the OS
import sys
try:
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO
gpio_powerrelay = 7
gpio_tfp3relay_pin = 3


#******************************************************************************************
def gpioInit(self):
    #global powerrelay_pin
    #global tfp3relay_pin
    #example
    # GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  PUD_UP
    # GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
    # add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
    # GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)
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
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]

