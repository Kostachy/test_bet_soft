from pydantic import BaseModel
import decimal
import enum


class EventState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Event(BaseModel):
    event_id: str
    coefficient: decimal.Decimal | None
    deadline: int | None
    state: EventState | None
