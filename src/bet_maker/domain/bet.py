from dataclasses import dataclass
from enum import Enum

from src.bet_maker.domain.value_object import BetSum


class BetState(Enum):
    WIN = "WIN"
    LOSE = "LOSE"
    PENDING = "PENDING"


@dataclass
class Bet:
    id: int | None
    state: BetState
    sum: BetSum
