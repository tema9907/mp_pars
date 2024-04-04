import asyncio
import json
from datetime import datetime

import aiohttp
from sqlalchemy import select

from database import Session
from models import Announce, Lot_announce
from queue_sendler import send_message_to_worker




async def add_new_announcement(json_data):
    # await asyncio.sleep(1)
    data = json_data
    async with Session() as session:

        stmt = select(Announce).where(Announce.announce_number == str(json_data.get('id')))
        result = await session.execute(stmt)
        announce = result.scalar_one_or_none()
        if announce is not None:
            print(f"Announce {announce.announce_number} already exists")
            return '1'
        try:
            announce = Announce(

                announce_number=str(data.get('id')),
                name=data.get('name_ru'),
                status_id='Опубликовано' if data.get('ref_buy_statuses_id') == 1 else 'Закрыт',
                type_id=data.get('tradeMethod').get('abbr'),
                purchase_method_id=data.get('tradeMethod').get('name_ru'),
                date_of_creation=datetime.strptime(data.get('create_date'), "%Y-%m-%dT%H:%M:%S.%fZ") if data.get('create_date') else None,
                offers_start_date=datetime.strptime(data.get('start_date'), "%Y-%m-%dT%H:%M:%S.%fZ") if data.get('start_date') else None,
                offers_end_date=datetime.strptime(data.get('refinement_end_date'), "%Y-%m-%dT%H:%M:%S.%fZ") if data.get(
                    'refinement_end_date') else datetime.strptime(data.get('end_date'),
                                                                  "%Y-%m-%dT%H:%M:%S.%fZ") if data.get(
                    'end_date') else None,
                organizer=data.get('organizer').get("bin") + " " + data.get('organizer').get('name_ru'),
                lots_quantity=len(data.get('lots')),
                sum_value=float(data.get("amount")) if data.get("amount") else None,
                url=f'https://eep.mitwork.kz/ru/publics/buy/{data.get("id")}',
                platform='mitwork',
                legal_address=data.get('organizer').get('address'),

            )

            session.add(announce)
            await session.commit()
            print(f"Announce {announce.announce_number} added")
        except Exception as e:
            print(e)
            return '0'

        for i in data.get('lots'):
            id = i.get('id')
            print(i.get('name_ru'))
            url = f"https://api.mitwork.kz/lots/{id}?key=3vh0BTWtRaYtU3GnhL4nAYZpu3ge47U7&expand=point,customer,places,files,justifications,status,unit"
            print(url)
            async with aiohttp.ClientSession() as http_session:
                for _ in range(5):
                    try:
                        async with http_session.get(url) as response:
                            response_text = await response.text()
                            lots = json.loads(response_text)
                            lot = Lot_announce(
                                announce_id=announce.id,
                                ktru_code=lots.get('ref_enstru_code'),
                                ktru_name=lots.get('name_ru'),
                                kato=str(lots['places'][0]['ref_kato_te']),
                                delivery_location=lots['places'][0]['address'] if lots.get('places') else None,
                                spec_url=','.join([file['_links']['self']['href'] for file in lots.get('files')]),
                                quantity=lots.get('count'),
                                brief_characteristics=lots.get('description_ru'),
                                additional_characteristics=lots.get('extra_description_ru'),
                                unit_price=float(lots.get('price')),
                                year1_amount=float(lots.get('point').get('amount_year_1')) if lots.get('point') else None,
                                year2_amount=float(lots.get('point').get('amount_year_2') )if lots.get('point') else None,
                                year3_amount=float(lots.get('point').get('amount_year_3')) if lots.get('point') else None,
                                planned_amount=float (lots.get('point').get('amount') )if lots.get('point') else None,
                                unit_measurement_id=lots.get('unit').get('name_ru'),
                                incoterms=lots.get('point').get('ref_incoterms_code') if lots.get('point') else None,
                                organizer_name=lots.get('customer').get('ref_kopf_code') + " " + lots.get('customer').get(
                                    'name_ru') if lots.get('customer') else data.get('organizer').get(
                                    "ref_kopf_code") + " " + data.get('organizer').get('name_ru'),
                                organizer_bin=lots.get('customer').get('bin') if lots.get('customer') else data.get(
                                    'organizer').get('bin'),
                                lot_number=str(lots.get('id')),
                                announce_number=str(announce.announce_number),
                                platform='mitwork',

                            )
                            announce.legal_address = lots.get("places")[0].get("address") if lots.get("places") else None

                            session.add(announce)
                            session.add(lot)
                            print(f"Lot {lot.id} added")
                            await session.commit()
                            await send_message_to_worker(lot.id)
                            break
                    except aiohttp.client_exceptions.ClientConnectorError:
                        print("Connection error, retrying in 5 seconds...")
                        session.rollback()
                        await asyncio.sleep(5)
                    except Exception as e:
                        print(1, e)
                        session.rollback()
                        break