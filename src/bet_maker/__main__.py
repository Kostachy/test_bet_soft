import asyncio

from src.bet_maker.config import load_config
from src.bet_maker.main import init_api, run_api


async def main() -> None:
    config = load_config()
    app = init_api(config)
    await run_api(app, config)


if __name__ == "__main__":
    asyncio.run(main())
