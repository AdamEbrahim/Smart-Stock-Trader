import asyncio

async def task1():
    i = 0
    while i < 3:
        print('doing task1 stuff')
        i = i + 1
        await asyncio.sleep(3)

async def task2():
    while True:
        print('doing task2 stuff')
        await asyncio.sleep(5)

async def task3():
    while True:
        print('doing task3 stuff')
        await asyncio.sleep(3)



async def main():
    print("starting main")
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())
    t3 = asyncio.create_task(task3())
    await t1
    while True:
        print("now back in main")
        await asyncio.sleep(3)

asyncio.run(main())