import logging
from functools import lru_cache
import time
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = "" # don't leave it empty. Set in .env
    chat_id: int = 0 # don't leave it empty. Set in .env

    # - request section -
    skiff_userid: str = "" # don't leave it empty. Set in .env
    skiff_secure: str = "" # don't leave it empty. Set in .env
    min_timestamp: int = int(time.time())
    scheluder_interval: int = 5 # the interval at which the mail is checked (in minutes)

    # - logging section -
    log_level: int = logging.INFO # level of logs (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    log_save: bool = True # save logs to file
    log_rich_formatter: bool = True # format logs with rich lib

    model_config = SettingsConfigDict(env_file='.env')

@lru_cache
def get_settings() -> Settings:
    return Settings()