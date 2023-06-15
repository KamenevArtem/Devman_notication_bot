import os
import time

import requests
import telegram

from dotenv import load_dotenv
from time import sleep


def get_user_reviews(headers):
    url = 'https://dvmn.org/api/user_reviews/'
    reviews_response = requests.get(url, headers=headers)
    reviews_response.raise_for_status()
    return reviews_response.json()


def long_polling_reviews(headers, chat_id, bot_token, timestamp):
    bot = telegram.Bot(token=bot_token)
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
    if review_description['status'] == 'found':
        notification_text = 'У Вас проверили работу, отправляем уведомление о проверке работ.'
        mistakes_notification_text = 'К сожалению в работе нашлись ошибки!'
        approved_text = 'Преподавателю все понравилось, можно приступать к следующему уроку'
        lesson_response = review_description['new_attempts']
        last_lesson_description = lesson_response[0]
        lesson_url = last_lesson_description['lesson_url']
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
    return timestamp


def main():
    load_dotenv()
    dev_access_token = os.environ['DEVMAN_API_TOKEN']
    bot_token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    headers = {
        'Authorization': f'Token {dev_access_token}'
    }
    timestamp = time.time()
    while True:
        try:
            print(timestamp)
            timestamp = long_polling_reviews(
                headers,
                chat_id,
                bot_token,
                timestamp
                )
        except (requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError):
            sleep(5)
            pass


if __name__ == '__main__':
    main()
