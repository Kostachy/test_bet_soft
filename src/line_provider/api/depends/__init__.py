import aio_pika
from aio_pika.pool import Pool
from fastapi import FastAPI

from src.line_provider.broker.factory import MessageBrokerFactory
from src.line_provider.broker.message_broker import MessageBroker


def setup_providers(
        app: FastAPI,
        pool: Pool[aio_pika.abc.AbstractChannel],
):
    bet_gateway_provider = MessageBrokerFactory(pool)

    app.dependency_overrides[MessageBroker] = bet_gateway_provider.create
