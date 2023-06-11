import os
import requests

from dotenv import load_dotenv
from pprint import pprint


def get_user_reviews(headers):
    url = 'https://dvmn.org/api/user_reviews/'
    reviews_response = requests.get(url, headers=headers)
    reviews_response.raise_for_status()


def long_polling_reviews(headers, timeout):
    url = 'https://dvmn.org/api/long_polling/'
    
    params = {
        'timestamp': {timeout}
    }
    while True:
        long_polling_response = requests.get(
            url,
            headers=headers,
            params=params
        )
        print(long_polling_response.url)
        long_polling_response.raise_for_status()
        pprint(long_polling_response.json())


def main():
    load_dotenv()
    access_token = os.environ['DEVMAN_API_TOKEN']
    headers = {
        'Authorization': f'Token {access_token}'
    }
    timeout = 5
    get_user_reviews(headers)
    long_polling_reviews(headers, timeout)


if __name__ == '__main__':
    try:
        main()
    except requests.exceptions.ReadTimeout:
        print('error')
        main()
