import time
from decimal import Decimal
from typing import Sequence

from src.bet_maker.application.common.event_client import EventClient
from src.bet_maker.infrastructure.http_client.schema import Event, EventState


class MockHttpClient(EventClient):
    async def get_all_available_events(self) -> Sequence[Event]:
        return [
            Event(
                event_id="1",
                coefficient=Decimal(1.2),
                deadline=int(time.time()) + 600,
                state=EventState.NEW,
            ),
            Event(
                event_id="2",
                coefficient=Decimal(1.15),
                deadline=int(time.time()) + 60,
                state=EventState.NEW,
            ),
            Event(
                event_id="3",
                coefficient=Decimal(1.67),
                deadline=int(time.time()) + 90,
                state=EventState.NEW,
            ),
        ]
