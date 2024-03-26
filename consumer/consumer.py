import asyncio
import logging
import os
from aiokafka import AIOKafkaConsumer, TopicPartition

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


async def consume_messages(consumer_id: str, topic: str, part: int, kafka_server: str):
    """
    функция для обработки сообщений из Kafka

    :param kafka_server: сервер Kafka
    :param consumer_id: id консьюмера
    :param topic: Название темы Kafka, из которой будут получены сообщения.
    :param part: Номер партиции, на которую подписывается консьюмер
    :return:
    """
    consumer = AIOKafkaConsumer(
        bootstrap_servers=kafka_server,
        group_id=consumer_id,
        enable_auto_commit=True,
        auto_offset_reset="earliest",
    )

    try:
        await consumer.start()

        topic_partition = TopicPartition(topic, part)           # подписываем консьюмера на топик и партицию
        consumer.assign([topic_partition])

        async for message in consumer:
            await asyncio.sleep(0.1)                            # симулируем обработку сообщения
            logging.info(f'{consumer_id} received message: {message.value.decode()}')

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        await consumer.stop()


async def main():
    kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS")         # сервер кафки
    consumer_id = os.getenv("CONSUMER_ID")                      # id группы из окружения
    topic = os.getenv("TOPIC")                                  # topic из окружения
    part = int(os.getenv("PART"))                               # номер партиции из окружения
    await consume_messages(consumer_id, topic, part, kafka_server)


asyncio.run(main())
