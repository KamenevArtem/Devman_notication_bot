import logging
import os
import time

import requests
import telegram

from dotenv import load_dotenv
from time import sleep

from tg_logger import TelegramLogsHandler


logger = logging.getLogger('Logger')


def get_review_description(
        headers,
        timestamp
        ):
    url = 'https://dvmn.org/api/long_polling/'
    params = {
        'timestamp': timestamp
    }
    long_polling_response = requests.get(
        url,
        headers=headers,
        params=params
    )
    long_polling_response.raise_for_status()
    review_description = long_polling_response.json()
    if 'last_attempt_timestamp' in review_description:
        timestamp = review_description['last_attempt_timestamp']
    return timestamp, review_description


def send_review(
        chat_id,
        bot,
        review_description
        ):
    if review_description['status'] == 'found':
        lesson_response = review_description['new_attempts']
        last_lesson_description = lesson_response[0]
        lesson_url = last_lesson_description['lesson_url']
        notification_text = 'У Вас проверили работу, отправляем уведомление о проверке работ.'
        mistakes_notification_text = 'К сожалению в работе нашлись ошибки!'
        approved_text = 'Преподавателю все понравилось, можно приступать к следующему уроку'
        if last_lesson_description['is_negative']:
                bot.send_message(
                    chat_id=chat_id,
                    text=f'{notification_text}\n{mistakes_notification_text}\n'
                    f'Ссылка на урок: {lesson_url}'
                    )
        else:
            bot.send_message(
                chat_id=chat_id,
                text=f'{notification_text}\n{approved_text}'
                )


def main():
    load_dotenv()
    dev_access_token = os.environ['DEVMAN_API_TOKEN']
    bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    logger_bot_token = os.environ['LOGGER_BOT_TOKEN']
    user_id = os.environ['USER_CHAT_ID']
    logger_bot = telegram.Bot(token=logger_bot_token)
    tg_bot = telegram.Bot(token=bot_token)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(logger_bot, user_id))
    headers = {
        'Authorization': f'Token {dev_access_token}'
    }
    logger.info('Бот запущен')
    timestamp = time.time()
    while True:
        try:
            timestamp, review_description = get_review_description(
                headers,
                timestamp
                )
            send_review(
                chat_id,
                tg_bot,
                review_description
                )
        except requests.exceptions.ConnectionError:
            logger.error('Ошибка соединения')
            sleep(5)
        except requests.exceptions.ReadTimeout:
            logger.error('Превышено время ожидания ответа')
            pass


if __name__ == '__main__':
    main()
