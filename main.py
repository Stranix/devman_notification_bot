import os
import requests

from pprint import pprint
from dotenv import load_dotenv

load_dotenv()


def send_request(url: str, token: str):
    headers = {
        'Authorization': 'Token {}'.format(token)
    }

    while True:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            pprint(response.json())
        except requests.exceptions.ReadTimeout:
            print('Тайм-аут ожидания ответа от сервера')
            print('Отправляю новый запрос')


def main():
    try:
        devman_token = os.environ['DEVMAN_TOKEN']
        url = 'https://dvmn.org/api/long_polling/'

        send_request(url, devman_token)
    except KeyError:
        print('Не задан токен в переменной окружения DEVMAN_TOKEN')


if __name__ == '__main__':
    main()
