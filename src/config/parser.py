from configparser import ConfigParser
from dataclasses import dataclass
from typing import List

from src.config.base_field import BaseSection


@dataclass
class Lolzteam(BaseSection):
    token: str
    search_urls_list: List[str]
    count: int


@dataclass
class Telegram(BaseSection):
    bot_token: str
    id: int


@dataclass
class Logging(BaseSection):
    level: int
    format: str


@dataclass
class Config:
    lolzteam: Lolzteam
    telegram: Telegram
    logging: Logging

    @classmethod
    def load_config(cls, filename: str) -> "Config":
        raw_config = ConfigParser()
        raw_config.read(filename, encoding="utf-8")
        if not raw_config.sections():
            raise FileNotFoundError(f"File {filename} is not defined")
        return cls(
            lolzteam=Lolzteam(**raw_config["lolzteam"]),
            telegram=Telegram(**raw_config["telegram"]),
            logging=Logging(**raw_config["logging"]),
        )
