from sys import platform
import time
from alpacaAPI import dailyProfitOrLoss

if platform == "linux": #If Linux (Raspberry Pi): 
    import board
    import RPi.GPIO as GPIO
    import neopixel


def LEDStripControl(api_key, secret_key):
    if platform == "linux": #If Linux (Raspberry Pi):
        pixel_pin = board.D18
        num_pixels = 60
        ORDER = neopixel.RGB
        pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
        pixels.fill((255, 0, 0))
        pixels.show()

        while True:
            profitOrLoss = dailyProfitOrLoss(api_key, secret_key)

            if profitOrLoss: #if profit
                print("profit")
                pixels.fill((255, 0, 0)) #green
                pixels.show()
            else: #if loss
                print("loss")
                pixels.fill((0, 255, 0)) #red
                pixels.show()

            time.sleep(300) #sleep for 5 minutes





if __name__ == '__main__':
    LEDStripControl()
