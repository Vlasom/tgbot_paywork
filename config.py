from dataclasses import dataclass
from environs import Env


@dataclass
class Bot:
    token: str  # gyТокен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    bot: Bot


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        bot=Bot(
            token=env('TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS')))
        ),
    )



