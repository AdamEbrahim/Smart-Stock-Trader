from gpiozero import MotionSensor


if __name__ == '__main__':
    gpio_pin = 17

    pir = MotionSensor(gpio_pin)

    while True:
        pir.wait_for_active()
        print("movement")
        pir.wait_for_inactive()