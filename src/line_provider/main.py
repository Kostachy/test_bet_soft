import logging

import aio_pika
import uvicorn
from aio_pika.pool import Pool
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.line_provider.api.depends import setup_providers
from src.line_provider.api.router import line_provider_router
from src.line_provider.config import Config

logger = logging.getLogger(__name__)


def init_api(pool: Pool[aio_pika.abc.AbstractChannel]) -> FastAPI:
    app = FastAPI(title="LineProviderAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_providers(app, pool)
    app.include_router(line_provider_router)
    return app


async def run_api(app: FastAPI, api_config: Config) -> None:
    config = uvicorn.Config(
        app,
        host=api_config.api.host,
        port=int(api_config.api.port),
        log_level=logging.INFO,
    )
    server = uvicorn.Server(config)
    logger.info("Running LineProviderAPI")
    await server.serve()
