import os
import sys

from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Settings:
    devman_api_url: str
    devman_token: str
    tg_api_url: str
    tg_bot_token: str
    tg_recipient_chat_id: int


def settings_init() -> Settings:
    try:
        return Settings(
            devman_api_url='https://dvmn.org/api/',
            devman_token=os.environ['DEVMAN_TOKEN'],
            tg_api_url='https://api.telegram.org/',
            tg_bot_token=os.environ['TG_BOT_TOKEN'],
            tg_recipient_chat_id=int(os.environ['RECIPIENT_CHAT_ID'])
        )
    except KeyError:
        print('Заданы не все переменные окружения.')
        sys.exit()


settings = settings_init()
