from sys import platform
import time
from datetime import datetime, timezone

if platform == "linux": #If Linux (Raspberry Pi): 
    #from gpiozero import MotionSensor
    import RPi.GPIO as GPIO

#screenOn and screenOff are callbacks
def motionDetection(gpio_pin, monitor_timeout, turnScreenOn, turnScreenOff):
    if platform == "linux": #If Linux (Raspberry Pi): 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin, GPIO.IN)

        timeout = monitor_timeout * 60 #convert minutes to seconds for timeout
        last_detection = datetime.now(timezone.utc)
        isScreenOn = True

        while True:
            if GPIO.input(gpio_pin):
                print("movement")
                last_detection = datetime.now(timezone.utc)
                if not isScreenOn:
                    turnScreenOn()
                    isScreenOn = True
            else:
                print("not any movement")
                if isScreenOn:
                    if (datetime.now(timezone.utc) - last_detection).total_seconds() > timeout:
                        turnScreenOff()
                        isScreenOn = False
            
            time.sleep(5)

    print("hi")