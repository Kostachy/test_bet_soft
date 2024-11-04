from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from aiohttp import ClientSession

from src.bet_maker.application.common.event_client import EventClient
from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.config import Config
from src.bet_maker.presentation.api.depends.bet_gateway_factory import BetGatewayFactory
from src.bet_maker.presentation.api.depends.http_client_factory import HttpEventClientFactory


def setup_providers(
        app: FastAPI,
        pool: async_sessionmaker[AsyncSession],
        http_session: ClientSession,
        config: Config
):
    bet_gateway_provider = BetGatewayFactory(pool)
    http_event_client_provider = HttpEventClientFactory(config, http_session)

    app.dependency_overrides[BetGateway] = bet_gateway_provider.create
    app.dependency_overrides[EventClient] = http_event_client_provider.create
