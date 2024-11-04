from decimal import Decimal

import pytest

from src.bet_maker.application.exceptions import NotAvailableEventForBetError
from src.bet_maker.application.usecases import bet_usecase
from src.tests.test_bet_maker.mock.mock_gateway import MockBetGateway
from src.tests.test_bet_maker.mock.mock_http_client import MockHttpClient


@pytest.mark.asyncio
async def test_create_bet(
        bet_gateway: MockBetGateway,
        http_client: MockHttpClient
):
    new_bet_id = await bet_usecase.make_bet(
        gateway=bet_gateway,
        event_client=http_client,
        bet_sum=Decimal(1.3),
        event_id="2",
    )
    assert new_bet_id == 6


@pytest.mark.asyncio
async def test_create_bet_with_exc(
        bet_gateway: MockBetGateway,
        http_client: MockHttpClient
):
    with pytest.raises(NotAvailableEventForBetError):
        await bet_usecase.make_bet(
            gateway=bet_gateway,
            event_client=http_client,
            bet_sum=Decimal(1.3),
            event_id="4",
        )


@pytest.mark.asyncio
async def test_get_all_available_events(
        http_client: MockHttpClient
):
    all_events = await bet_usecase.get_all_available_events(event_client=http_client)

    assert all_events
    assert len(all_events) > 0
