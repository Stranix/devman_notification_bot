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
