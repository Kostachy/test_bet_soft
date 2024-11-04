from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    database_url: str


@dataclass
class LineProviderClientConfig:
    url: str
    timeout: int


@dataclass
class ApiConfig:
    host: str = "0.0.0.0"
    port: int = 8080


@dataclass
class BrokerConfig:
    broker_url: str


@dataclass
class Config:
    database: DatabaseConfig
    line_provider_client: LineProviderClientConfig
    api: ApiConfig
    broker: BrokerConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        database=DatabaseConfig(database_url=env("DATABASE_URL")),
        line_provider_client=LineProviderClientConfig(
            url=env("LINE_PROVIDER_URL"),
            timeout=env("LINE_PROVIDER_TIMEOUT"),
        ),
        api=ApiConfig(
            host=env("BET_MAKER_HOST"),
            port=env("BET_MAKER_PORT"),
        ),
        broker=BrokerConfig(broker_url=env("BROKER_URL")),
    )
