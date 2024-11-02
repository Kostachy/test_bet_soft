import logging
from fastapi import FastAPI


def create_line_provider_app() -> FastAPI:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # settings = load_config()
    app_ = FastAPI(title="LineProviderAPI")
    return app_


app = create_line_provider_app()
