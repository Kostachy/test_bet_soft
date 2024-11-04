import pytest

from src.tests.test_bet_maker.mock.mock_gateway import MockBetGateway
from src.tests.test_bet_maker.mock.mock_http_client import MockHttpClient


@pytest.fixture()
def bet_gateway() -> MockBetGateway:
    return MockBetGateway()


@pytest.fixture()
def http_client() -> MockHttpClient:
    return MockHttpClient()
