from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.bet_maker.infrastructure.db.gateway.bet_gateway import SqlBetGateway


class BetGatewayFactory:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def create(self):
        async with self.pool() as session:
            yield SqlBetGateway(session=session)
