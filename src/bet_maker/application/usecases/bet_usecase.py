import logging
from decimal import Decimal
from typing import Sequence

from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.domain.bet import Bet, BetState
from src.bet_maker.domain.value_object import BetSum

logger = logging.getLogger(__name__)


async def make_bet(gateway: BetGateway, bet_sum: Decimal) -> int:
    bet_sum_obj = BetSum(bet_sum)
    bet = Bet(
        id=None,
        state=BetState.PENDING,
        sum=bet_sum_obj.to_raw(),
    )
    new_bet_id = await gateway.create_bet(bet)
    await gateway.commit()

    logger.info("Bet with id %s was created", new_bet_id)

    return new_bet_id


async def get_all_bets(gateway: BetGateway) -> Sequence[Bet]:
    all_bets = await gateway.get_all_bets()
    return all_bets
