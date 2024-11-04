import asyncio

from src.line_provider.broker.factory import create_connection_pool, create_channel_pool
from src.line_provider.config import load_config
from src.line_provider.main import run_api, init_api


async def main() -> None:
    config = load_config()
    connection_pool = await create_connection_pool(config)
    channel_pool = await create_channel_pool(connection_pool)
    app = init_api(channel_pool)
    await run_api(app, config)


if __name__ == "__main__":
    asyncio.run(main())