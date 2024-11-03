from decimal import Decimal

from fastapi import APIRouter, Depends
from typing import Annotated

from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.application.usecases import bet_usecase
from src.bet_maker.domain.bet import Bet
from src.bet_maker.presentation.api.depends.depends_stub import Stub
from src.bet_maker.presentation.api.router.dtos.bet import BetSumDto, BetIdDto

bet_router = APIRouter()


@bet_router.get("/events")
async def get_all_available_events():
    pass


@bet_router.post("/bet", response_model=BetIdDto)
async def make_bet(
        bet_sum_dto: BetSumDto,
        bet_gateway: Annotated[BetGateway, Depends(Stub(BetGateway))]
):
    new_bet_id = await bet_usecase.make_bet(bet_gateway, bet_sum_dto.bet_sum)
    return {"id": new_bet_id}


@bet_router.get("/bets", response_model=list[Bet])
async def get_all_bets(bet_gateway: Annotated[BetGateway, Depends(Stub(BetGateway))]):
    all_available_bets = await bet_gateway.get_all_bets()
    return all_available_bets
