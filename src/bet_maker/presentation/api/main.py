import logging

from fastapi import FastAPI

from src.bet_maker.config import load_config
from src.bet_maker.infrastructure.db.factory import create_engine, create_session_maker
from src.bet_maker.presentation.api.router.bet_router import bet_router


def create_bet_maker_app():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    settings = load_config()
    engine = create_engine(database_url=settings.database.database_url)
    session_maker = create_session_maker(engine)

    app_ = FastAPI()
    app_.include_router(bet_router)

    return app_


app = create_bet_maker_app()
