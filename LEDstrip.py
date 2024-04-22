from sys import platform
import time
from alpacaAPI import dailyProfitOrLoss

if platform == "linux": #If Linux (Raspberry Pi): 
    import board
    import RPi.GPIO as GPIO
    import neopixel


def LEDStripControl(api_key, secret_key, led_pin, led_pixels):
    if platform == "linux": #If Linux (Raspberry Pi):
        pixel_pin = 0
        if led_pin == 18:
            pixel_pin = board.D18
        elif led_pin == 10:
            pixel_pin = board.D10
        elif led_pin == 12:
            pixel_pin = board.D12
        elif led_pin == 21:
            pixel_pin = board.D21
        else:
            print("invalid pin to control LED strip, please use one of GPIO 10, 12, 18, 21")
            return

        
        num_pixels = led_pixels
        ORDER = neopixel.RGB
        pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
        pixels.fill((255, 0, 0))
        pixels.show()

        while True:
            profitOrLoss = dailyProfitOrLoss(api_key, secret_key)

            if profitOrLoss: #if profit
                print("profit")
                pixels.fill((0, 255, 0)) #green
                pixels.show()
            else: #if loss
                print("loss")
                pixels.fill((0, 255, 0)) #red
                pixels.show()

            time.sleep(300) #sleep for 5 minutes





if __name__ == '__main__':
    LEDStripControl()
