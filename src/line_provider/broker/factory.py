import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractChannel
from aio_pika.pool import Pool

from .message_broker import RMQMessageBroker, MessageBroker
from ..config import Config


async def get_robust_connection(config: Config) -> AbstractRobustConnection:
    return await aio_pika.connect_robust(url=config.broker.broker_url)


async def create_connection_pool(config: Config, max_size: int = 5):
    return Pool(lambda: get_robust_connection(config), max_size=max_size)


async def get_channel(connection_pool: Pool[aio_pika.abc.AbstractConnection]) -> AbstractChannel:
    async with connection_pool.acquire() as connection:
        return await connection.channel(publisher_confirms=True)


async def create_channel_pool(connection_pool: Pool[aio_pika.abc.AbstractConnection], max_size: int = 10):
    return Pool(lambda: get_channel(connection_pool), max_size=max_size)


# Решил не использовать транзакции, чтобы излишне не усложнять
#
# async def build_rq_transaction(
#         rq_channel: aio_pika.abc.AbstractChannel,
# ) -> aio_pika.abc.AbstractTransaction:
#     rq_transaction = rq_channel.transaction()
#     await rq_transaction.select()
#     return rq_transaction

class MessageBrokerFactory:
    def __init__(self, rq_channel_pool: Pool[aio_pika.abc.AbstractChannel]):
        self.rq_channel_pool = rq_channel_pool

    async def create(self) -> MessageBroker:
        async with self.rq_channel_pool.acquire() as channel:
            # channel.transaction()
            yield RMQMessageBroker(channel)
