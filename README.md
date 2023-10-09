# Devman_notification_bot

Скрипт осуществляющий оповещение пользователя о статусе проверки работ обучающих курсов [Devman.org](https://dvmn.org/). Оповещения реализованы через передачу ботом сообщений в Telegram.

## Как установить

Python3 версии 3.11 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

## Как запустить

Необходимо скачать репозиторий проекта, затем создать файл `.env` в корневой папке проекта. В данный файл необходимо внести переменные окружения:

* `DEVMAN_API_TOKEN` - токен API Devman. Получить его можно, пройдя по [ссылке](https://dvmn.org/api/docs/);

* `TG_BOT_TOKEN` - токен бота. Он может быть получен сразу после создания бота. [Инструкция по созданию бота](https://habr.com/ru/articles/262247/);

* `CHAT_ID` - id чата пользователя. Для получения необходимо написать в Telegram специальному боту: [@userinfobot](https://telegram.me/userinfobot);

* `USER_CHAT_ID` - id чата пользователя для получения инОрмации об ошибках;

* `LOGGER_BOT_TOKEN` - токен второго бота, предназначенного для отслеживания ошибок.

Cкрипт запускается командой:

```
python3 bot.py
```
на MacOs/Linux и
```
python bot.py
```
на Windows


## Как запустить бота при помощи docker

- Убедитесь что у вас установлен docker. Про [установку docker](https://docs.docker.com/get-docker/).
- Соберите докер образ текущего проекта запустив команду:


```
docker build --tag notification_bot .
``` 
Подробнее про [docker build images](https://docs.docker.com/language/python/build-images/).

- Через команду 
```
docker run  --restart=always --env-file .env notification_bot
```
запустите докер контейнер на основе собранного ранее образа проекта.
- В случае успешного запуска докер контейнера, в телеграм придет следующее сообщение: `Бот запущен`
  
- Для остановки работы контейнера используйте команду 
```
docker stop CONTAINER_ID
```
Узнать CONTAINER_ID можно выполнив команду `docker ps`. [Подробнее про run containers](https://docs.docker.com/language/python/run-containers/).

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [devman](https://dvmn.org/)


