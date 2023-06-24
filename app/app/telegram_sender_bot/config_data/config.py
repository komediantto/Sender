
from dataclasses import dataclass
from app.core.config import settings


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:
    return Config(tg_bot=TgBot(token=settings.BOT_TOKEN))
