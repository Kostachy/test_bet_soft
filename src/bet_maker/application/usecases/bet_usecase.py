import logging
from decimal import Decimal
from typing import Sequence

from src.bet_maker.application.common.event_client import EventClient
from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.application.exceptions import NotAvailableEventForBetError
from src.bet_maker.domain.bet import Bet, BetState
from src.bet_maker.domain.value_object import BetSum
from src.bet_maker.infrastructure.http_client.schema import EventState, Event

logger = logging.getLogger(__name__)


async def make_bet(gateway: BetGateway, event_client: EventClient, bet_sum: Decimal, event_id: str) -> int:
    all_available_events = await event_client.get_all_available_events()
    for event in all_available_events:
        if event.event_id == event_id and event.state == EventState.NEW:
            bet_sum_obj = BetSum(bet_sum)
            bet = Bet(
                id=None,
                state=BetState.PENDING,
                sum=bet_sum_obj.to_raw(),
                event_id=event_id
            )
            new_bet_id = await gateway.create_bet(bet)
            await gateway.commit()

            logger.info("Bet with id %s was created", new_bet_id)

            return new_bet_id
    raise NotAvailableEventForBetError(event_id)


async def update_bet_state_if_event_state_was_updated(gateway: BetGateway, event: Event) -> None:
    bets = await gateway.get_all_bets_with_event_id(event.event_id)
    for bet in bets:
        if bet.event_id == event.event_id:
            if event.state == EventState.FINISHED_WIN:
                bet.update_state(BetState.WIN)
            elif event.state == EventState.FINISHED_LOSE:
                bet.update_state(BetState.LOSE)
            else:
                continue
            updated_bet_id = await gateway.update_bet(bet)

            logger.info("Bet with id %s was updated", updated_bet_id)
    await gateway.commit()


async def get_all_available_events(event_client: EventClient) -> Sequence[Event]:
    all_available_events = await event_client.get_all_available_events()
    return all_available_events


async def get_all_bets(gateway: BetGateway) -> Sequence[Bet]:
    all_bets = await gateway.get_all_bets()
    return all_bets
