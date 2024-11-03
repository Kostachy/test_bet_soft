from pydantic import BaseModel, condecimal


class BetSumDto(BaseModel):
    bet_sum: condecimal(max_digits=10, decimal_places=2)


class BetIdDto(BaseModel):
    id: int
