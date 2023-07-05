import sys

from dotenv import load_dotenv

from services import start_polling


def main():
    try:
        start_polling()
    except KeyError:
        print('Заданы не все настройки переменных окружения.')
        sys.exit()


if __name__ == '__main__':
    try:
        load_dotenv()
        main()
    except KeyboardInterrupt:
        print('Работа остановлена')
        sys.exit()
