import asyncio
import time

async def brew(name):
    print(f"Brewing {name}...")
    #await asyncio.sleep(2)  means wait in non blocking fashion
    time.sleep(3)
    print(f"{name} is ready...")

async def main():
   
   await asyncio.gather(
       brew("Masala Chai"), 
       brew("Green Chai"), 
       brew("Ginger Chai")
       )
#you are waiting only for two second for three operations

asyncio.run(main()) 