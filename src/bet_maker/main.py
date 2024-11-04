import logging

import uvicorn
from fastapi import FastAPI
from aiohttp import ClientSession
from src.bet_maker.config import Config
from src.bet_maker.infrastructure.db.factory import create_engine, create_session_maker
from src.bet_maker.presentation.api.depends import setup_providers
from src.bet_maker.presentation.api.router.bet_router import bet_router
from src.bet_maker.presentation.api.router.exceptions import setup_exception_handlers

logger = logging.getLogger(__name__)


def init_api(config: Config):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    http_session = ClientSession()
    engine = create_engine(database_url=config.database.database_url)
    session_maker = create_session_maker(engine)

    app_ = FastAPI(title="BetMakerApi")

    setup_providers(app_, session_maker, http_session, config)
    setup_exception_handlers(app_)

    app_.include_router(bet_router)

    return app_


async def run_api(app: FastAPI, api_config: Config) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.api.host,
        port=int(api_config.api.port),
        log_level=logging.INFO,
        log_config=None
    )
    server = uvicorn.Server(config)
    logger.info("Running BetMakerApi")
    await server.serve()
