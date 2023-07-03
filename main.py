import sys

from services import start_polling


def main():
    try:
        start_polling()
    except KeyboardInterrupt:
        print('Работа остановлена')
        sys.exit()


if __name__ == '__main__':
    main()
