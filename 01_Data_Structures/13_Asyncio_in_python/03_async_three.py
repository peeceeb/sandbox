import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        print(f"Fetched {url} with status {response.status}")

async def main():
    urls=["https://httpbin.org/delay/2"] * 3
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        await asyncio.gather(*tasks)  #Web requests for 3 will be resposnded in 3 arrays. #arr1,arr2,arr3 OR can be written as .gather(t1, t2, t3)

asyncio.run(main())