
import aio_pika
import uuid
import traceback
from config import Config


async def send_message_to_worker(lot_id: uuid):
    print("===============RABBIT MQ WORKER==================")

    try:
        print(f"Sending message to worker {lot_id}")
        uuid_str = lot_id
        uuid_bytes = uuid_str.bytes
        connection = await aio_pika.connect_robust(Config.MQCONNECTION)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("new_lot", durable=True)
            await channel.default_exchange.publish(aio_pika.Message(body=uuid_bytes), routing_key=queue.name)
            print(f"Sent meg: {queue.name} - {lot_id}")
    except Exception as e:
        traceback.print_exc()
        print(e)