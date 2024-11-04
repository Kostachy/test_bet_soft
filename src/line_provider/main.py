import logging

import aio_pika
import uvicorn
from aio_pika.pool import Pool
from fastapi import FastAPI

from src.line_provider.api.depends import setup_providers
from src.line_provider.broker.factory import get_robust_connection, create_connection_pool, create_channel_pool
from src.line_provider.config import Config
from src.line_provider.logging import LOGGING_CONFIG
from src.line_provider.api.router import line_provider_router

logger = logging.getLogger(__name__)


async def get_connection_pool(config: Config):
    connection_pool = await create_connection_pool(config)
    channel_pool = create_channel_pool(connection_pool)

def init_api(pool: Pool[aio_pika.abc.AbstractChannel]) -> FastAPI:
    app = FastAPI(title="LineProviderAPI")
    setup_providers(app, pool)
    app.include_router(line_provider_router)
    return app


async def run_api(app: FastAPI, api_config: Config) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.api.host,
        port=api_config.api.port,
        log_level=logging.INFO,
        log_config=LOGGING_CONFIG,
    )
    server = uvicorn.Server(config)
    logger.info("Running LineProviderAPI")
    await server.serve()
