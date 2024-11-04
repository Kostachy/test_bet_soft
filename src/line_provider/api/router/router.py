import time
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Depends

from src.line_provider.api.depends.depends_stub import Stub
from src.line_provider.broker.message import Message
from src.line_provider.broker.message_broker import MessageBroker
from src.line_provider.storage import Event, events

line_provider_router = APIRouter()


@line_provider_router.put('/event')
async def create_event(
        event: Event,
        message_broker: Annotated[MessageBroker, Depends(Stub(MessageBroker))]
):
    """event_id
coefficient
deadline
state"""
    if event.event_id not in events:
        events[event.event_id] = event
        await message_broker.declare_exchange("bet_event")
        await message_broker.publish_message(
            message=Message(
                message_id=uuid4(),
                data={
                    "event_id": event.event_id,
                    "coefficient": str(event.coefficient),
                    "deadline": event.deadline,
                    "state": str(event.state)
                },
                message_type="event",
            ),
            routing_key="event",
            exchange_name="bet_event",
        )
        return {}

    for p_name, p_value in event.model_dump(exclude_unset=True).items():
        setattr(events[event.event_id], p_name, p_value)

    return {}


@line_provider_router.get('/event/{event_id}')
async def get_event(event_id: str | None = None):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail="Event not found")


@line_provider_router.get('/events')
async def get_events():
    return list(e for e in events.values() if time.time() < e.deadline)
