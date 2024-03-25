import asyncio
import logging
import os
from aiokafka import AIOKafkaConsumer

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


async def consume_messages(consumer_id: str, topic: str, key: str):
    """
    функция для обработки сообщений из Kafka

    :param consumer_id: id консьюмера
    :param topic: Название темы Kafka, из которой будут получены сообщения.
    :param key: Ключ, по которому отбираются сообщения для обработки.
    :return:
    """
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers="kafka:9092",
        group_id=consumer_id,
        enable_auto_commit=True,
        auto_offset_reset="earliest",

    )

    try:
        await consumer.start()
        async for message in consumer:
            if message.key == key.encode('utf-8'):  # проверяем кто должен обработать сообщение
                await asyncio.sleep(0.1)            # симулируем обработку сообщения
                logging.info(f'{consumer_id} received message: {message.value.decode()}')

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        await consumer.stop()


async def main():
    consumer_id = os.getenv("CONSUMER_ID")     # id группы из окружения
    topic = os.getenv("TOPIC")                  # topic из окружения
    key = os.getenv("KEY")                      # key из окружения
    await consume_messages(consumer_id, topic, key)


asyncio.run(main())
