import signal
import time

def handler(signum, frame):
    print("time: " + time.ctime())

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, handler)
    signal.setitimer(signal.ITIMER_REAL, 5)
    while True:
        time.sleep(1)