import logging
from typing import Sequence

import aiohttp
from aiohttp.client_exceptions import ConnectionTimeoutError

from src.bet_maker.application.common.event_client import EventClient
from src.bet_maker.infrastructure.http_client.schema import Event

logger = logging.getLogger(__name__)


class HttpEventClient(EventClient):
    def __init__(self, url: str, timeout: int, session: aiohttp.ClientSession):
        self.session = session
        self.url = url
        self.timeout = timeout

    async def get_all_available_events(self) -> Sequence[Event]:
        async with self.session.get(url=self.url) as request:
            try:
                response = await request.json()
                if request.status != 200:
                    logger.info(
                        "Get an error when trying to make request to line_provider's events. Status code is %s",
                        request.status,
                    )
                    return []
                return [Event(**event) for event in response]
            except ConnectionTimeoutError:
                logger.error(
                    "Get timeout when make request to line_provider events",
                    exc_info=True,
                )
                return []
