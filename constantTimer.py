from threading import Thread, Timer
import time

class constantTimer:
    def __init__(self, time, handle):
        self.time = time
        self.handle = handle
        self.timer = Timer(self.time, self.timerHandler)

    def timerHandler(self):
        self.handle()
        self.timer = Timer(self.time, self.timerHandler)
        self.timer.start()

    def start(self):
        self.timer.start()

    def cancel(self):
        self.timer.cancel()

def printer():
    print("curr time: " + time.ctime())

if __name__ == '__main__':

    tim = constantTimer(5, printer)
    tim.start() #start creates a new thread responsible for the timer

    while True:
        print("hi lol it iisn't blokign")
        time.sleep(.1)
    