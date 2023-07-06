import os
import argparse

from dotenv import load_dotenv

from services import start_polling


def create_arg_parser():
    description = 'Отправляем уведомления о проверке уроков devman в telegram'

    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('chat_id', metavar='', type=int,
                            help='''id телеграм чата куда бот будет отправлять
                            уведомления.
                            '''
                            )
    return arg_parser


def main():
    try:
        load_dotenv()
        args = create_arg_parser().parse_args()
        devman_token = os.environ['DEVMAN_TOKEN']
        tg_bot_token = os.environ['TG_BOT_TOKEN']
        tg_recipient_chat_id = args.chat_id
        start_polling(devman_token, tg_bot_token, tg_recipient_chat_id)
    except KeyError:
        print('Заданы не все настройки переменных окружения.')
    except KeyboardInterrupt:
        print('Работа остановлена')


if __name__ == '__main__':
    main()
