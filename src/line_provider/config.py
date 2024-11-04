from dataclasses import dataclass

from environs import Env


@dataclass
class BrokerConfig:
    broker_url: str


@dataclass
class ApiConfig:
    host: str = "0.0.0.0"
    port: int = 8100


@dataclass
class Config:
    broker: BrokerConfig
    api: ApiConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        broker=BrokerConfig(broker_url=env("BROKER_URL")),
        api=ApiConfig(
            host=env("LINE_PROVIDER_HOST"),
            port=env("LINE_PROVIDER_PORT"),
        )
    )
