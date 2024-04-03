import asyncio
import concurrent.futures
import time

def task1():
    while True:
        print('doing task1 stuff')
        time.sleep(.25)
        # for i in range(100000):
        #     print('doing task1 stuff')
        # for i in range(100000):
        #     print("task 1 going to sleep")
        # time.sleep(5)


def task2():
    while True:
        print('doing task2 stuff')
        time.sleep(.25)



def task3():
    while True:
        print('doing task3 stuff')
        time.sleep(.25)


executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
executor.submit(task1)
executor.submit(task2)
executor.submit(task3)

while True:
    print("main stuff")
    time.sleep(.25)
