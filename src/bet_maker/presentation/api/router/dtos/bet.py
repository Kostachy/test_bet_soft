from pydantic import BaseModel, condecimal


class BetCreateDto(BaseModel):
    bet_sum: condecimal(max_digits=10, decimal_places=2)
    event_id: str


class BetIdDto(BaseModel):
    id: int
