import os
import requests

from pprint import pprint
from dotenv import load_dotenv

load_dotenv()


def main():
    try:
        devman_token = os.environ['DEVMAN_TOKEN']

        url = 'https://dvmn.org/api/long_polling/'
        headers = {
            'Authorization': 'Token {}'.format(devman_token)
        }

        while True:
            response = requests.get(url, headers=headers)
            pprint(response.json())
    except KeyError:
        print('Не задан токен в переменной окружения DEVMAN_TOKEN')


if __name__ == '__main__':
    main()
