from decimal import Decimal
from typing import Sequence

from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.domain.bet import Bet, BetState
from src.bet_maker.domain.value_object import BetSum


class BetUseCase:
    def __init__(self, gateway: BetGateway):
        self._gateway = gateway

    async def make_bet(self, bet_sum: Decimal) -> None:
        bet_sum_obj = BetSum(bet_sum)
        bet = Bet(
            id=None,
            state=BetState.PENDING,
            sum=bet_sum_obj,
        )
        await self._gateway.create_bet(bet)
        await self._gateway.commit()

    async def get_all_bets(self) -> Sequence[Bet]:
        all_bets = await self._gateway.get_all_bets()
        return all_bets
