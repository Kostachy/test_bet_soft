from faststream import Logger
from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitRouter

from src.bet_maker.application.usecases import bet_usecase as bet_service
from src.bet_maker.infrastructure.consumer.depends import create_bet_gateway
from src.bet_maker.infrastructure.consumer.schema import Message

rabbit_router = RabbitRouter()
exchange = RabbitExchange("bet_event")
queue_1 = RabbitQueue("event_queue", durable=True, routing_key="event")


@rabbit_router.subscriber(queue_1, exchange)
async def base_handler1(logger: Logger, event: Message):
    logger.info(f"Event with id {event.data.event_id}")
    bet_gateway = await create_bet_gateway()
    await bet_service.update_bet_state_if_event_state_was_updated(
        bet_gateway, event.data
    )
