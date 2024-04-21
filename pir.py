from sys import platform
import time

if platform == "linux": #If Linux (Raspberry Pi): 
    #from gpiozero import MotionSensor
    import RPi.GPIO as GPIO


def motionDetection(gpio_pin):
    if platform == "linux": #If Linux (Raspberry Pi): 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN)

        while True:
            if GPIO.input(gpio_pin):
                print("movement")
            else:
                print("not any movement")
            
            time.sleep(5)

    print("hi")