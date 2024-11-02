from dataclasses import dataclass


class DomainError(Exception):
    """Base Domain Error"""


@dataclass
class InvalidBetSumError(DomainError):

    @property
    def description(self) -> str:
        return "Неверная сумма ставки. Сумма должна быть больше 0"
