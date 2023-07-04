# Отправка уведомлений о проверенных работах
Работы проверенные в процессе обучения на платформе [dvmn.org](https://dvmn.org/)

### Требования
* Python версии: `python=> 3.10`
* Заполненные переменные окружения
    * `DEVMAN_TOKEN` - токен платформы devman. Инструкция [здесь](https://dvmn.org/api/docs/).
    * `TG_BOT_TOKEN` - токен телеграм бота, который будет отправлять сообщения. Как получить читать [здесь](https://lifehacker.ru/kak-sozdat-bota-v-telegram/).
* Наличие идентификатора чата телеграм куда будут отправляться сообщения. Как пример можно прочитать [здесь](https://lumpics.ru/how-find-out-chat-id-in-telegram/).

### Как запустить
* Скачиваем репозиторий
```shell
git clone https://github.com/Stranix/devman_notification_bot.git
```
* Устанавливаем зависимости
```shell
pip install -r requirements.txt
```
* Запускаем скрипт с указанием телеграм `chat_id`
```shell
python main.py 909090909090
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).