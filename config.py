import os
import sys
import argparse

from dataclasses import dataclass


@dataclass
class Settings:
    devman_api_url: str
    devman_token: str
    tg_api_url: str
    tg_bot_token: str
    tg_recipient_chat_id: int


def create_arg_parser():
    description = 'Отправляем уведомления о проверке уроков devman в telegram'

    arg_parser = argparse.ArgumentParser(
        description=description,
    )

    arg_parser.add_argument('chat_id', metavar='', type=int,
                            help='''id телеграм чата куда бот будет отправлять
                            уведомления.
                            '''
                            )

    return arg_parser


def settings_init() -> Settings:
    """Инициализируем настройки которые нужны для работы приложения"""
    parser = create_arg_parser()
    args = parser.parse_args()
    return Settings(
        devman_api_url='https://dvmn.org/api/',
        devman_token=os.environ['DEVMAN_TOKEN'],
        tg_api_url='https://api.telegram.org/',
        tg_bot_token=os.environ['TG_BOT_TOKEN'],
        tg_recipient_chat_id=args.chat_id
    )


settings = settings_init()
