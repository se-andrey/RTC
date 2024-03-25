import asyncio
import logging
import os

from aiokafka import AIOKafkaProducer


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


async def producer_messages():
    """
    Функция для отправки сообщений в Kafka.
    :return:
    """

    producer = AIOKafkaProducer(
        bootstrap_servers="kafka:9092",
    )

    try:
        await producer.start()

        topic = os.getenv("TOPIC")
        messages = ((b"Message 1", b"key1"), (b"Message 2", b"key2"))
        index = 0

        while True:

            message, key = messages[index % 2]          # делим сообщения между двумя консьюмерами
            await producer.send_and_wait(topic, message, key=key)
            logging.info(f"Message sent: {message.decode()}")
            index += 1
            await asyncio.sleep(5)

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        await producer.stop()


asyncio.run(producer_messages())

