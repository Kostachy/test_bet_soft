from dataclasses import dataclass


class ApplicationError(Exception):
    """Base application error"""

    pass


@dataclass
class NotAvailableEventForBetError(ApplicationError):
    event_id: str

    @property
    def description(self) -> str:
        return f"Event c id {self.event_id} на данный момент недоступен для ставок"
