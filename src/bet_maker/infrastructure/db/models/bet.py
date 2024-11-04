from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

from src.bet_maker.domain.bet import BetState
from src.bet_maker.infrastructure.db.models.base import TimedBaseModel


class Bet(TimedBaseModel):
    __tablename__ = "bets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    state: Mapped[BetState] = mapped_column(default=BetState.PENDING)
    sum: Mapped[Decimal]
    event_id: Mapped[str]
