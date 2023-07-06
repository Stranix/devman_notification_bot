import time

import requests

from urllib.parse import urljoin


def create_notification_message(attempt: dict) -> str:
    """Создаем информационное сообщение для отправки в телеграм чат.

    :param attempt: словарь с информацией о проверенном уроке.

    :return: информационное сообщение.
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


def start_polling(
        devman_token: str,
        tg_bot_token: str,
        tg_recipient_chat_id: int,
        timeout: int = 95):
    """Запускаем долгие запросы на Devman API.

    В случаи обнаружения проверенной работы будет отправлено уведомление
    в телеграм чат.

    :param devman_token: токен авторизации devman api.
    :param tg_bot_token: токен телеграм бота который будет отправлять сообщения.
    :param tg_recipient_chat_id: время ожидания ответа от сервера. По умолчанию 95 сек.
    :param timeout: время ожидания ответа от сервера. По умолчанию 95 сек.
    """
    devman_api_url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': 'Token {}'.format(devman_token),
    }
    params = {}
    while True:
        try:
            response = requests.get(
                devman_api_url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            devman_review = response.json()

            if devman_review['status'] == 'timeout':
                params['timestamp'] = devman_review['timestamp_to_request']
                print('Задан параметр timestamp', devman_review['timestamp_to_request'])

            if devman_review['status'] == 'found':
                params['timestamp'] = devman_review['last_attempt_timestamp']
                for attempt in devman_review['new_attempts']:
                    notification_message = create_notification_message(attempt)

                    send_message_from_tg_bot(
                        tg_bot_token,
                        tg_recipient_chat_id,
                        notification_message
                    )
        except requests.exceptions.HTTPError as err:
            print(err.response)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print(
                'Нет соединения. Попробуем отправить повторный запрос через '
                '5 сек'
            )
            time.sleep(5)


def send_message_from_tg_bot(
        token: str,
        chat_id: int,
        message: str,
        parse_mode: str = 'HTML'
):
    """Отправляем сообщение через телеграм бота в чат.

    Настройки chat_id берется из параметров скрипта при старте.

    :param token: токен телеграм бота, который отправляет сообщение.
    :param chat_id: телеграм чат id куда отправляем сообщение.
    :param message: сообщение для отправки.
    :param parse_mode: режим парсинга сообщения со стороны телеграм. По умолчанию 'HTML'.

    """
    print('Отправка сообщения через телеграм бота')
    send_message_url = urljoin(
        'https://api.telegram.org/',
        f'/bot{token}/sendMessage',
    )

    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': parse_mode,
    }

    response = requests.get(send_message_url, params=params)
    response.raise_for_status()
    tg_api = response.json()

    if not tg_api.get('ok'):
        print('Не смог отправить сообщение')
