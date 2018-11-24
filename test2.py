import time
import asyncio

async def do_some_work(x):
    print("Waiting " + str(x))
    await asyncio.sleep(x)

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(do_some_work(2)), 
         asyncio.ensure_future(do_some_work(5))]

loop.run_until_complete(asyncio.gather(*tasks))

tasks.