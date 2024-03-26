import asyncio
import logging
import os

from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


async def create_topic_if_not_exists(topic_name: str, kafka_server: str):
    """
    Проверяет и создает топик на с 2я партициями и 1м фактором репликации

    :param topic_name: Название топика
    :param kafka_server: сервер Kafka
    :return:
    """
    admin_client = AIOKafkaAdminClient(bootstrap_servers=kafka_server)
    await admin_client.start()

    topics = await admin_client.list_topics()

    if topic_name not in topics:
        new_topic = NewTopic(topic_name, num_partitions=2, replication_factor=1)
        result = await admin_client.create_topics([new_topic])
        logging.info(f"Topic '{topic_name}' make {result}")
    else:
        logging.info(f"Topic '{topic_name}' exist")

    await admin_client.close()


async def producer_messages(topic_name: str, kafka_server: str):
    """
    Функция для отправки сообщений в Kafka.

    :param topic_name: Название топика
    :param kafka_server: сервер Kafka
    :return:
    """

    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_server,
    )

    try:
        await producer.start()

        messages = ((b"Message 1", b"key1"), (b"Message 2", b"key2"))
        index = 0

        while True:
            part = index % 2
            message, key = messages[index % 2]          # делим сообщения между двумя консьюмерами
            await producer.send(topic_name, message, key=key, partition=part)
            logging.info(f"Message sent: {message.decode()}")
            index += 1
            await asyncio.sleep(5)

    except Exception as e:
        logging.error(f"Error: {e}")

    finally:
        await producer.stop()


async def main():
    topic_name = os.getenv("TOPIC")
    kafka_server = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    await create_topic_if_not_exists(topic_name, kafka_server)
    await producer_messages(topic_name, kafka_server)


if __name__ == "__main__":
    asyncio.run(main())

