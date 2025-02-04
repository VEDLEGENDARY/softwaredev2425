import asyncio
import time 
import aiohttp
import requests
import json

regions = ['us']
results = []

async def get_news():
    async with aiohttp.ClientSession() as session:
        for region in regions:
            # print('Getting {}'.format(region))
            response = await session.get("https://newsapi.org/v2/top-headlines?country={}&apiKey=d1fe035fe8494498b5505023fcddd3e0".format(region), ssl=False)
            results.append(await response.json())



def get_news2():
    for region in regions:
        # print('Getting {}'.format(region))
        response = requests.get("https://newsapi.org/v2/top-headlines?country={}&apiKey=d1fe035fe8494498b5505023fcddd3e0".format(region))
        results.append(response.json())
        

################

# async def get_tasks(session):
#     # Define list of tasks
#     tasks = []
#     for region in regions:
#         # Add the function to the list of tasks
#         with session.get("https://newsapi.org/v2/top-headlines?country={}&apiKey=d1fe035fe8494498b5505023fcddd3e0".format(region)) as response:
#             print(await response.json())

#     return tasks


# async def get_news3():
#     # Opens up a new http session
#     async with aiohttp.ClientSession() as session:
#         # Calls the get_tasks() function
#         tasks = await get_tasks(session)
#         # Gets the return value from the get_tasks() function
#         responses = await asyncio.gather(*tasks)
#         print(responses)
#         for response in responses:
#             results.append(await response.json())


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        for region in regions:
            url = "https://newsapi.org/v2/top-headlines?country={}&apiKey=d1fe035fe8494498b5505023fcddd3e0".format(region)   # Example URL that returns JSON data
            json_data = await fetch(session, url)
            print(json.dumps(json_data, indent=4))  # Pretty-print the JSON data



print("<----Call to 10 API endpoints time trial---->\n")
# start = time.time()
# get_news2()
# end = time.time()
# print(f"[Python Requests]: {end - start} secs to complete\n")

# start = time.time()
# asyncio.run(get_news())
# end = time.time()
# print(f"[Async + aiohttp]: {end - start} secs to complete\n")

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
end = time.time()
print(f"[Async tasks]: {end - start} secs to complete\n")
