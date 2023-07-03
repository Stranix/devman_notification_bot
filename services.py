import time
import requests

from urllib.parse import urljoin

from config import settings


def create_notification_message(attempt: dict) -> str:
    lesson_title = attempt['lesson_title']
    lesson_url = attempt['lesson_url']

    message = f'У вас проверили работу\n<code>{lesson_title}</code>\n\n'
    if attempt['is_negative']:
        message += 'В работе нашлись ошибки\n'
    else:
        message += 'Работа принята!\n'
    message += lesson_url
    return message


def start_polling():
    params = {}
    while True:
        try:
            response = send_request(params)
            response.raise_for_status()
            devman_api = response.json()

            if devman_api['status'] == 'timeout':
                params['timestamp'] = devman_api['timestamp_to_request']
                print('Задан параметр timestamp',
                      devman_api['timestamp_to_request'])

            if devman_api['status'] == 'found':
                params['timestamp'] = devman_api['last_attempt_timestamp']
                for attempt in devman_api['new_attempts']:
                    notification_message = create_notification_message(attempt)
                    tg_bot_send_message(notification_message)
        except requests.exceptions.HTTPError:
            print('Ошибка HTTP. Код ответа не 200')
        except requests.exceptions.ReadTimeout:
            print('Тайм-аут ожидания ответа от сервера')
        except requests.exceptions.ConnectionError:
            print(
                'Нет соединения. Попробуем отправить повторный запрос через '
                '5 сек'
            )
            time.sleep(5)


def send_request(params: dict, timeout=95) -> requests.Response:
    url = urljoin(settings.devman_api_url, 'long_polling/')
    print('Отправка запроса на', url, 'с параметрами', params)
    headers = {
        'Authorization': 'Token {}'.format(settings.devman_token),
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=timeout
    )
    response.raise_for_status()
    print('Запрос выполнен')
    return response


def tg_bot_send_message(
        message: str,
        parse_mode: str = 'HTML'
):
    print('Отправка сообщения через телеграм бота')
    tg_bot_url = urljoin(settings.tg_api_url, f'/bot{settings.tg_bot_token}')
    send_message_url = tg_bot_url + '/sendMessage'
    params = {
        'chat_id': settings.tg_recipient_chat_id,
        'text': message,
        'parse_mode': parse_mode,
    }

    response = requests.get(send_message_url, params=params)
    tg_api = response.json()
    print(tg_api)
    if not tg_api['ok']:
        raise requests.exceptions.HTTPError
