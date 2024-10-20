from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    db_user: str
    db_password: str
    db_name: str
    host: str


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID"),
            db_user=env.str("DB_USER"),
            db_password=env.str("DB_PASSWORD"),
            db_name=env.str("DB_NAME"),
            host=env.str("HOST")
        )
    )


settings = get_settings('input')