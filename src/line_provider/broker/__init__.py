import aio_pika


async def setup_broker():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()  # Создание нового канала
        queue = await channel.declare_queue("test_queue", durable=True)
        exchange = await channel.declare_exchange("test_exchange", aio_pika.ExchangeType.DIRECT)
