import time

import requests

from typing import Any
from urllib.parse import urljoin

from config import settings


def create_notification_message(attempt: dict) -> str:
    """Создаем информационное сообщение для отправки в телеграм чат.

    :param attempt: dict - словарь с информацией о проверенном уроке.

    :return: str - информационное сообщение.
    """
    lesson_title = attempt['lesson_title']
    lesson_url = attempt['lesson_url']

    message = f'У вас проверили работу\n<code>{lesson_title}</code>\n\n'
    if attempt['is_negative']:
        message += 'В работе нашлись ошибки\n'
    else:
        message += 'Работа принята!\n'
    message += lesson_url
    return message


def start_polling(timeout: int = 95):
    """Запускаем долгие запросы на Devman API.

    В случаи обнаружения проверенной работы будет отправлено уведомление
    в телеграм чат.

    :param timeout: int - время ожидания ответа от сервера. По умолчанию 95 сек
    """
    params = {}
    while True:
        try:
            response = send_request(params, timeout)
            response.raise_for_status()
            devman_api_response = response.json()

            if devman_api_response['status'] == 'timeout':
                params['timestamp'] = devman_api_response['timestamp_to_request']
                print('Задан параметр timestamp',
                      devman_api_response['timestamp_to_request'])

            if devman_api_response['status'] == 'found':
                params['timestamp'] = devman_api_response['last_attempt_timestamp']
                for attempt in devman_api_response['new_attempts']:
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


def send_request(params: dict, timeout: Any = None) -> requests.Response:
    """Отправляем запросы на указанный url.

    Настройки url берутся из переменных окружения.

    В случаи обнаружения проверенной работы будет отправлено уведомление
    в телеграм чат.

    :param params: параметры запроса в виде словаря.
    :param timeout: время ожидания ответа от сервера. По умолчанию None.

    :return: requests.Response - объект успешного ответа.
    """
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
    """Отправляем сообщение через телеграм бота в чат.

    Настройки chat_id берется из параметров скрипта при старте.

    :param message: str - сообщение для отправки.
    :param parse_mode: str - режим парсинга сообщения со стороны телеграм. По умолчанию 'HTML'.

    """
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

    if not tg_api['ok']:
        raise requests.exceptions.HTTPError
