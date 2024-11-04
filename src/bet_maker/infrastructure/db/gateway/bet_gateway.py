import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.bet_maker.application.common.gateway import BetGateway
from src.bet_maker.domain.bet import Bet
from src.bet_maker.domain.value_object import BetSum
from src.bet_maker.infrastructure.db.models import Bet as BetDb

logger = logging.getLogger(__name__)


class SqlBetGateway(BetGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_bet_by_id(self, id_: int) -> Bet | None:
        query = select(BetDb).where(BetDb.id == id_)
        result = await self.session.execute(query)
        bet = result.scalar_one_or_none()
        if bet is None:
            return None
        return Bet(
            id=bet.id,
            state=bet.state,
            sum=bet.sum,
            event_id=bet.event_id
        )

    async def get_all_bets(self) -> Sequence[Bet]:
        query = select(BetDb).order_by(BetDb.created_at)
        result = await self.session.execute(query)
        all_bets = result.scalars().all()
        if not all_bets:
            return []
        return [
            Bet(
                id=bet.id,
                state=bet.state,
                sum=bet.sum,
                event_id=bet.event_id
            ) for bet in all_bets
        ]

    async def get_all_bets_with_event_id(self, event_id: str) -> Sequence[Bet]:
        query = select(BetDb).where(BetDb.event_id == event_id).order_by(BetDb.created_at)
        result = await self.session.execute(query)
        all_bets = result.scalars().all()
        if not all_bets:
            return []
        return [
            Bet(
                id=bet.id,
                state=bet.state,
                sum=bet.sum,
                event_id=bet.event_id
            ) for bet in all_bets
        ]

    async def create_bet(self, bet: Bet) -> int:
        db_bet = BetDb(
            sum=bet.sum,
            event_id=bet.event_id
        )
        self.session.add(db_bet)
        try:
            await self.session.flush((db_bet,))
        except IntegrityError:
            logger.error("Error in BetGateway")
        return db_bet.id

    async def update_bet(self, bet: Bet) -> int:
        db_bet = BetDb(
            id=bet.id,
            state=bet.state,
            sum=bet.sum,
            event_id=bet.event_id
        )
        await self.session.merge(db_bet)
        try:
            await self.session.flush((db_bet,))
        except IntegrityError:
            logger.error("Error in BetGateway")
        return db_bet.id

    async def commit(self) -> None:
        await self.session.commit()
