import asyncio

async def brew_chai():
    print("Brewing Chai....")
    await asyncio.sleep(2) #Doesn't block your main thread.
    print("Chai is ready")

asyncio.run(brew_chai())