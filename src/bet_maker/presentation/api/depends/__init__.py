from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.presentation.api.depends.bet_gateway_factory import BetGatewayFactory


def setup_providers(
        app: FastAPI,
        pool: async_sessionmaker[AsyncSession],
):
    bet_gateway_provider = BetGatewayFactory(pool)

    app.dependency_overrides[BetGateway] = bet_gateway_provider.create
