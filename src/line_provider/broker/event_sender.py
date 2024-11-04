from abc import abstractmethod
from typing import Protocol
from uuid import uuid4

from src.line_provider.broker.message import Message
from src.line_provider.broker.message_broker import MessageBroker
from src.line_provider.storage import Event


class EventSender(Protocol):

    @abstractmethod
    def send_event(self, event: Event):
        raise NotImplementedError


class ImpEventSender(EventSender):
    def __init__(self, message_broker: MessageBroker):
        self.message_broker = message_broker

    async def send_event(self, event: Event):
        await self.message_broker.declare_exchange("bet_event")
        await self.message_broker.publish_message(
            message=Message(
                message_id=uuid4(),
                data={
                    "event_id": event.event_id,
                    "coefficient": float(event.coefficient),
                    "deadline": event.deadline,
                    "state": event.state.value
                },
                message_type="event",
            ),
            routing_key="event",
            exchange_name="bet_event",
        )
