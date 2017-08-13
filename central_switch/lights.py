import RPi.GPIO as GPIO
import time
import os

class Lights:
    def __init__(self):
        # Define PiLITEr to GPIO mapping
        #self.leds = [13]
        #GPIO.setmode(GPIO.BCM)
        #for pin in self.leds:
            #GPIO.setup(pin, GPIO.OUT)

    def hide(self):
        #leds = self.leds
        #for pin in leds:
            #GPIO.output(pin, GPIO.LOW)

    def show(self):
        #leds = self.leds
        #for pin in leds:
            #GPIO.output(pin, GPIO.HIGH)

    def cleanup(self):
        #GPIO.cleanup()

