from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.config import load_config
from src.bet_maker.infrastructure.db.factory import create_engine, create_session_maker
from src.bet_maker.infrastructure.db.gateway.bet_gateway import SqlBetGateway

config = load_config()
engine = create_engine(config.database.database_url)
session_maker = create_session_maker(engine)


async def create_bet_gateway() -> BetGateway:
    async with session_maker() as session:
        return SqlBetGateway(session)
