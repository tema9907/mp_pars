import aiohttp
import asyncio
from datetime import datetime as dt

from crud import add_new_announcement
from config import Config


async def get_buy_details(session, id):
    url = f"https://api.mitwork.kz/buys/{id}"
    params = {
        "key": Config.API_KEY,
        "expand": "lots,organizer,files,lots.files,status,type,tradeMethod"
    }
    async with session.get(url, params=params) as response:
        data = await response.json()
        await add_new_announcement(data)

async def parse_endpoint():
    url = "https://api.mitwork.kz/buys"
    params = {
        "sort": "ref_buy_statuses_id",
        "key": Config.API_KEY,
        "size": "10",
    }

    while True:
        ids = []
        async with aiohttp.ClientSession() as session:
            print("=============Parsing started=============")
            for page in range(1, 500):
                params["page"] = str(page)
                print(f"Requesting page {page}")
                async with session.get(url, params=params) as response:
                    data = await response.json()
                    for item in data:
                        if item.get('refinement_end_date') and dt.strptime(item.get('refinement_end_date'), "%Y-%m-%dT%H:%M:%S.%fZ") >= dt.now():
                            ids.append(item.get('id'))
                            continue
                        if item.get('end_date') and dt.strptime(item.get('end_date'), "%Y-%m-%dT%H:%M:%S.%fZ")>= dt.now():
                            ids.append(item.get('id'))
                            continue
                    if any(item.get('ref_buy_statuses_id') == 2 for item in data):
                        print(f"Found 'ref_buy_statuses_id': 2 on page {page}")
                        break
            else:
                continue
            print(f"Found {len(ids)} open announcements")
            tasks = [get_buy_details(session, id) for id in ids]
            await asyncio.gather(*tasks)
        print("=============Parsing finished=============")
        await asyncio.sleep(30)

loop = asyncio.get_event_loop()
loop.run_until_complete(parse_endpoint())