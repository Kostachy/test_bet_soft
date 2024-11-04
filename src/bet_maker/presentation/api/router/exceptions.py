import logging
from dataclasses import dataclass

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from src.bet_maker.application.exceptions import (
    ApplicationError,
    NotAvailableEventForBetError,
)
from src.bet_maker.domain.exceptions import DomainError, InvalidBetSumError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ErrorResult:
    error: str
    error_description: str


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(DomainError, bet_exception_handler)
    app.add_exception_handler(ApplicationError, bet_exception_handler)
    app.add_exception_handler(Exception, unknown_exception_handler)


async def bet_exception_handler(
    request: Request, err: Exception
) -> ORJSONResponse:  # noqa
    match err:
        case InvalidBetSumError() as err:
            return ORJSONResponse(
                ErrorResult(
                    error=err.__class__.__name__, error_description=err.description
                ),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case NotAvailableEventForBetError() as err:
            return ORJSONResponse(
                ErrorResult(
                    error=err.__class__.__name__, error_description=err.description
                ),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        case _:
            logger.exception("Unknown error occurred", exc_info=err)
            return ORJSONResponse(
                ErrorResult(
                    error="Unknown server error",
                    error_description="Упс... Что-то пошло не так, попробуйте позже.",
                ),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


async def unknown_exception_handler(
    request: Request, err: Exception
) -> ORJSONResponse:  # noqa
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResult(
            error="Unknown server error",
            error_description="Unknown server error has occurred",
        ),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
