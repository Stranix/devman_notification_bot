import os
import sys

from pprint import pprint
from dotenv import load_dotenv

import services

load_dotenv()


def main():
    try:
        devman_token = os.environ['DEVMAN_TOKEN']
        tg_bot_token = os.environ['TG_BOT_TOKEN']
        tg_recipient_chat_id = os.environ['RECIPIENT_CHAT_ID']
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
                services.tg_bot_send_message(
                    tg_bot_token,
                    int(tg_recipient_chat_id),
                    'Преподаватель проверил работу',
                )
    except KeyError:
        print('Заданы не все переменные окружения.')
    except KeyboardInterrupt:
        print('Работа остановлена')
    finally:
        sys.exit()


if __name__ == '__main__':
    main()

