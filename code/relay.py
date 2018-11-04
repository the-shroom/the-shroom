import time

import RPi.GPIO as GPIO

pin = 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)

time.sleep(0.25)

GPIO.output(pin, GPIO.HIGH)
GPIO.cleanup()