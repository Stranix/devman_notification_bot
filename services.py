import time
import requests


def send_long_pooling_request(
        url: str,
        token: str,
        params: dict,
        timeout=95
) -> requests.Response:
    headers = {
        'Authorization': 'Token {}'.format(token),
    }
    while True:
        try:
            print('Отправка запроса на', url)
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout
            )
            response.raise_for_status()
            print('Выполнен запрос на ', response.url)
            return response
        except requests.exceptions.HTTPError:
            print('Ошибка HTTP. Код ответа не 200')
        except requests.exceptions.ReadTimeout:
            print('Тайм-аут ожидания ответа от сервера')
        except requests.exceptions.ConnectionError:
            print(
                'Нет интернета. Попробуем отправить повторный запрос через '
                '5 сек'
            )
            time.sleep(5)


def tg_bot_send_message(
        tg_bot_token: str,
        chat_id: int,
        message: str,
        parse_mode: str = 'HTML'
):
    tg_url = 'https://api.telegram.org/bot{}/sendMessage'.format(tg_bot_token)
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': parse_mode,
    }

    response = requests.get(tg_url, params=params)
    tg_api = response.json()
    print(tg_api)
    if not tg_api['ok']:
        raise requests.exceptions.HTTPError
