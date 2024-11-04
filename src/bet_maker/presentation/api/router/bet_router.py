from fastapi import APIRouter, Depends
from typing import Annotated

from src.bet_maker.application.common.event_client import EventClient
from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.application.usecases import bet_usecase
from src.bet_maker.domain.bet import Bet
from src.bet_maker.infrastructure.http_client.schema import Event
from src.bet_maker.presentation.api.depends.depends_stub import Stub
from src.bet_maker.presentation.api.router.dtos.bet import BetCreateDto, BetIdDto

bet_router = APIRouter()


@bet_router.get("/events", response_model=list[Event])
async def get_all_available_events(event_client: Annotated[EventClient, Depends(Stub(EventClient))]):
    all_available_events = await bet_usecase.get_all_available_events(event_client)
    return all_available_events


@bet_router.post("/bet", response_model=BetIdDto)
async def make_bet(
        bet_sum_dto: BetCreateDto,
        bet_gateway: Annotated[BetGateway, Depends(Stub(BetGateway))],
        event_client: Annotated[EventClient, Depends(Stub(EventClient))]
):
    new_bet_id = await bet_usecase.make_bet(bet_gateway, event_client, bet_sum_dto.bet_sum, bet_sum_dto.event_id)
    return {"id": new_bet_id}


@bet_router.get("/bets", response_model=list[Bet])
async def get_all_bets(bet_gateway: Annotated[BetGateway, Depends(Stub(BetGateway))]):
    all_available_bets = await bet_usecase.get_all_bets(bet_gateway)
    return all_available_bets
