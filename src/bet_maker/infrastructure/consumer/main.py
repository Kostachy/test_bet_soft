from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.bet_maker.config import load_config
from src.bet_maker.infrastructure.consumer.router import rabbit_router


def create_consumer():
    config = load_config()
    broker = RabbitBroker(url=config.broker.broker_url)
    broker.include_router(rabbit_router)

    app_ = FastStream(broker)
    return app_


app = create_consumer()
