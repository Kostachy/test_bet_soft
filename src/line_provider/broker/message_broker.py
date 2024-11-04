import json
import logging
from typing import Protocol

import aio_pika
from aio_pika.abc import AbstractChannel

from .message import Message


class MessageBroker(Protocol):
    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        raise NotImplementedError

    async def declare_exchange(self, exchange_name: str) -> None:
        raise NotImplementedError


class RMQMessageBroker(MessageBroker):
    def __init__(self, channel: AbstractChannel) -> None:
        self._channel = channel

    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        body = {
            "message_type": message.message_type,
            "data": message.data,
        }

        rq_message = aio_pika.Message(
            body=json.dumps(body).encode(),
            message_id=str(message.message_id),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            headers={},
        )

        exchange = await self._channel.get_exchange(exchange_name, ensure=False)
        queue = await self._channel.declare_queue("event_queue", durable=True)
        await queue.bind(exchange, routing_key=routing_key)

        await exchange.publish(rq_message, routing_key=routing_key)

        logging.info("Message with id %s was send", rq_message.message_id)

    async def declare_exchange(self, exchange_name: str) -> None:
        await self._channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.DIRECT
        )
