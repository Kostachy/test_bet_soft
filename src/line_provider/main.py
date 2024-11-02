import logging
from fastapi import FastAPI

from src.line_provider.router import line_provider_router


def create_line_provider_app() -> FastAPI:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # settings = load_config()
    app_ = FastAPI(title="LineProviderAPI")
    app_.include_router(line_provider_router)
    return app_


app = create_line_provider_app()
