from abc import abstractmethod
from typing import Protocol

from src.line_provider.broker.message_broker import MessageBroker


class EventSender(Protocol):
    def __init__(self, message_broker: MessageBroker):
        self.message_broker = message_broker

    @abstractmethod
    def send_event(self):
        raise NotImplementedError
