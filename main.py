import sys

from dotenv import load_dotenv

from services import start_polling


def main():
    try:
        start_polling()
    except KeyboardInterrupt:
        print('Работа остановлена')
        sys.exit()


if __name__ == '__main__':
    load_dotenv()
    main()
