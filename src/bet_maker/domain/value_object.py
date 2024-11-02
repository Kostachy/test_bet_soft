from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from marshmallow.fields import Decimal

from src.bet_maker.domain.exceptions import InvalidBetSumError

V = TypeVar("V", bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC):
    """Базовый класс для Объектов-значений"""

    def __post_init__(self) -> None:
        """Данный метод валидирует поля объекта после инициализации его атрибутов"""
        self._validate()

    def _validate(self) -> None:
        """Этот метод проверяет допустимость значения для создания этого объекта-значения."""


@dataclass(frozen=True)
class ValueObject(BaseValueObject, ABC, Generic[V]):
    """Базовый класс для Объектов-значений с конвертацией"""
    value: V

    def to_raw(self) -> V:
        return self.value


from dataclasses import dataclass


@dataclass(frozen=True)
class BetSum(ValueObject[Decimal]):
    """Объект-значение для валидации суммы ставки"""
    value: Decimal

    def _validate(self) -> None:
        if not self.value:
            raise InvalidBetSumError()
        if self.value < Decimal(0):
            raise InvalidBetSumError()
