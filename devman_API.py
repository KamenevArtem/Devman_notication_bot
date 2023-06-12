import os
import requests

from dotenv import load_dotenv
from pprint import pprint


def get_user_reviews(headers):
    url = 'https://dvmn.org/api/user_reviews/'
    reviews_response = requests.get(url, headers=headers)
    reviews_response.raise_for_status()
    return reviews_response.json()


def long_polling_reviews(headers, timeout):
    url = 'https://dvmn.org/api/long_polling/'
    long_polling_response = requests.get(
        url,
        headers=headers,
        timeout=timeout
    )
    long_polling_response.raise_for_status()
    pprint(long_polling_response.json())
    return long_polling_response.json()


def main():
    load_dotenv()
    access_token = os.environ['DEVMAN_API_TOKEN']
    headers = {
        'Authorization': f'Token {access_token}'
    }
    timeout = 3
    get_user_reviews(headers)
    while True:
        try:
            long_polling_reviews(headers, timeout)
        except (requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError):
            pass


if __name__ == '__main__':
    main()
