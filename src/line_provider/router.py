import time
from fastapi import APIRouter, HTTPException

from src.line_provider.storage import Event, events

line_provider_router = APIRouter()


@line_provider_router.put('/event')
async def create_event(event: Event):
    if event.event_id not in events:
        events[event.event_id] = event
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
