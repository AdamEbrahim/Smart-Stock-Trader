from gpiozero import MotionSensor

gpio_pin = 17

pir = MotionSensor(gpio_pin)

while True:
    pir.wait_for_active()
    print("movement")
    pir.wait_for_inactive()