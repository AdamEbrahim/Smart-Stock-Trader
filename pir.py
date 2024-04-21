from sys import platform
import time

<<<<<<< HEAD

if __name__ == '__main__':
    gpio_pin = 17

    pir = MotionSensor(gpio_pin)

    while True:
        pir.wait_for_active()
        print("movement")
        pir.wait_for_inactive()
=======
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
>>>>>>> 5153fa8fea34a83de85c609f43775fec58c933dc
