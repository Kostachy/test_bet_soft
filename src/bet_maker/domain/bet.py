from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class BetState(Enum):
    WIN = "WIN"
    LOSE = "LOSE"
    PENDING = "PENDING"


@dataclass
class Bet:
    id: int | None
    state: BetState
    sum: Decimal
    event_id: str

    def update_state(self, state: BetState):
        self.state = state
