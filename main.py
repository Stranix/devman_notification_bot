import os
import time
import requests

from pprint import pprint
from dotenv import load_dotenv

load_dotenv()


def send_request(url: str, token: str, timeout=95):
    headers = {
        'Authorization': 'Token {}'.format(token)
    }

    while True:
        try:
            print('Отправка запроса на', url)
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            pprint(response.json())
        except requests.exceptions.ReadTimeout:
            print('Тайм-аут ожидания ответа от сервера')
        except requests.exceptions.ConnectionError:
            print(
                'Нет интернета. Попробуем отправить повторный запрос через '
                '5 сек'
            )
            time.sleep(5)


def main():
    try:
        devman_token = os.environ['DEVMAN_TOKEN']
        url = 'https://dvmn.org/api/long_polling/'

        send_request(url, devman_token)
    except KeyError:
        print('Не задан токен в переменной окружения DEVMAN_TOKEN')


if __name__ == '__main__':
    main()
