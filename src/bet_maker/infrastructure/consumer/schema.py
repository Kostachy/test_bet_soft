from pydantic import BaseModel

from src.bet_maker.infrastructure.http_client.schema import Event


class Message(BaseModel):
    message_type: str
    data: Event
