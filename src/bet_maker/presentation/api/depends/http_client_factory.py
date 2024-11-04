from aiohttp import ClientSession

from src.bet_maker.config import Config
from src.bet_maker.infrastructure.http_client.event_client import HttpEventClient


class HttpEventClientFactory:
    def __init__(self, config: Config, http_session: ClientSession):
        self.http_session = http_session
        self.config = config

    def create(self) -> HttpEventClient:
        return HttpEventClient(
            session=self.http_session,
            url=self.config.line_provider_client.url,
            timeout=self.config.line_provider_client.timeout,
        )
