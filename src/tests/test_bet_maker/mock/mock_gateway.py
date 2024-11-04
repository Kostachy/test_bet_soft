from decimal import Decimal
from typing import Sequence

from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.domain.bet import Bet, BetState


class MockBetGateway(BetGateway):
    async def get_bet_by_id(self, id_: int) -> Bet | None:
        return Bet(
            id=1,
            state=BetState.WIN,
            sum=Decimal(999.9),
            event_id="2",

        )

    async def get_all_bets(self) -> Sequence[Bet]:
        raise [
            Bet(
                id=1,
                state=BetState.WIN,
                sum=Decimal(999.9),
                event_id="2",

            ),
            Bet(
                id=2,
                state=BetState.LOSE,
                sum=Decimal(119.9),
                event_id="3",

            ),
            Bet(
                id=3,
                state=BetState.PENDING,
                sum=Decimal(12.3),
                event_id="4",

            ),
            Bet(
                id=4,
                state=BetState.PENDING,
                sum=Decimal(299.3),
                event_id="4",

            )
        ]

    async def get_all_bets_with_event_id(self, event_id: str) -> Sequence[Bet]:
        return [
            Bet(
                id=3,
                state=BetState.PENDING,
                sum=Decimal(12.3),
                event_id="4",

            ),
            Bet(
                id=4,
                state=BetState.PENDING,
                sum=Decimal(299.3),
                event_id="4",

            )
        ]

    async def create_bet(self, bet: Bet) -> int:
        return 6

    async def update_bet(self, bet: Bet) -> int:
        return 6

    async def commit(self) -> None:
        return None
