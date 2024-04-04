import json
import aiohttp
import asyncio
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from database import Session
from models import Announce
from datetime import datetime as dt
from config import Config

# engine = create_async_engine(Config.DB_CONNECTION_STRING, echo=True, future=True)

async def fetch_status(session, announce):
    url = f"https://api.mitwork.kz/buys/{announce.announce_number}?key={Config.API_KEY}&expand=status"
    async with session.get(url) as response:
        if response.status == 200:

            response_text = await response.text()
            response_json = json.loads(response_text)
            if response_json.get('end_date') and dt.strptime(response_json.get('end_date'), "%Y-%m-%dT%H:%M:%S.%fZ") < dt.now():
                if response_json.get('refinement_end_date') and dt.strptime(response_json.get('refinement_end_date'),
                                                                   "%Y-%m-%dT%H:%M:%S.%fZ") < dt.now():
                    announce.status_id = 'Закрыт'
                    print(f"Announce {announce.announce_number} status updated to Закрыт")
                    return
            new_status = 'Опубликовано' if response_json.get('ref_buy_statuses_id') == 1 else 'Закрыт'
            if new_status != announce.status_id:
                announce.status_id = new_status
                print(f"Announce {announce.announce_number} status updated to {new_status}")

async def update_announcements():

    while True:
        logging.info('======================Update announcements task started======================')
        await asyncio.sleep(30)
        stmt = select(Announce).where(Announce.status_id == 'Опубликовано')
        async with Session() as session:
            result = await session.execute(stmt)
        open_announcements = result.scalars().all()
        print(f"Found {len(open_announcements)} open announcements")
        async with aiohttp.ClientSession() as http_session:
            tasks = [fetch_status(http_session, announce) for announce in open_announcements]
            await asyncio.gather(*tasks)
            async with Session() as session:
                session.add_all(open_announcements)
                await session.commit()
        print('===============================Update finished===============================')

    logging.info('Update announcements task finished')
asyncio.run(update_announcements())