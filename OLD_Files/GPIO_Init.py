import RPi.GPIO as GPIO


class gpioInit():
    #example
    # GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  PUD_UP
    # GPIO.setup(channel, GPIO.OUT, initial=GPIO.HIGH)
    # add rising edge detection on a channel, ignoring further edges for 200ms for switch bounce handling
    # GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=200)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    powerrelay_pin = 7
    tfp3relay_pin = 3
    GPIO.setup(powerrelay_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(tfp3relay_pin, GPIO.OUT, initial=GPIO.LOW)
    gpio_on = 1
    gpio_off = 0

def main():
    pass



if __name__ == '__main__':
    main()

