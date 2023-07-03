import os
import sys

from pprint import pprint
from dotenv import load_dotenv

import services

load_dotenv()


def main():
    try:
        devman_token = os.environ['DEVMAN_TOKEN']
        url = 'https://dvmn.org/api/long_polling/'
        params = {}
        while True:
            response = services.send_long_pooling_request(
                url=url,
                token=devman_token,
                params=params,
            )
            devman_api = response.json()

            if devman_api['status'] == 'timeout':
                params['timestamp'] = devman_api['timestamp_to_request']
                print('Задан параметр timestamp', devman_api['timestamp_to_request'])

            if devman_api['status'] == 'found':
                params['timestamp'] = devman_api['last_attempt_timestamp']
                pprint(devman_api)
    except KeyError:
        print('Не задан токен в переменной окружения DEVMAN_TOKEN')
    except KeyboardInterrupt:
        print('Работа остановлена')
    finally:
        sys.exit()


if __name__ == '__main__':
    main()

