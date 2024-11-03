from decimal import Decimal
from typing import Protocol, Sequence
from abc import abstractmethod

from src.bet_maker.domain.bet import Bet


class BetGateway(Protocol):
    @abstractmethod
    async def get_bet_by_id(self, id_: int) -> Bet | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_bets(self) -> Sequence[Bet]:
        raise NotImplementedError

    @abstractmethod
    async def create_bet(self, bet: Bet) -> int:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError
