import time
import asyncio
from concurrent.futures import ThreadPoolExecutor ##Pull all threads together

def check_stock(item):
    print(f"Checking {item} in store..")
    time.sleep(3)
    return f"{item} stock: 42"

async def main():
    loop=asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool,check_stock,"Masala Chai")
        print(result)

asyncio.run(main())
