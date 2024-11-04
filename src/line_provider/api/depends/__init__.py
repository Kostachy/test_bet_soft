import aio_pika
from aio_pika.pool import Pool
from fastapi import FastAPI

from src.line_provider.broker.event_sender import EventSender
from src.line_provider.broker.factory import EventSenderFactory


def setup_providers(
        app: FastAPI,
        pool: Pool[aio_pika.abc.AbstractChannel],
):
    event_sender_provider = EventSenderFactory(pool)

    app.dependency_overrides[EventSender] = event_sender_provider.create
