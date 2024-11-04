from typing import Protocol, Sequence
from abc import abstractmethod

from src.bet_maker.infrastructure.http_client.schema import Event


class EventClient(Protocol):

    @abstractmethod
    async def get_all_available_events(self) -> Sequence[Event]:
        raise NotImplementedError
