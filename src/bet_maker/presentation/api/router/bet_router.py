from fastapi import APIRouter

bet_router = APIRouter()


@bet_router.get("/events")
async def get_all_available_events():
    pass


@bet_router.post("/bet")
async def make_bet():
    pass


@bet_router.get("/bets")
async def get_all_bets():
    pass
