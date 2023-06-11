import os
import requests

from dotenv import load_dotenv
from pprint import pprint


def main():
    load_dotenv()
    access_token = os.environ['DEVMAN_API_TOKEN']
    reviews_url = 'https://dvmn.org/api/user_reviews/'
    headers = {
        'Authorization': f'Token {access_token}'
    }
    reviews_response = requests.get(reviews_url, headers=headers)
    reviews_response.raise_for_status()
    long_polling_url = 'https://dvmn.org/api/long_polling/'
    while True:
        long_polling_response = requests.get(
            long_polling_url,
            headers=headers,
        )
        long_polling_response.raise_for_status()
        pprint(long_polling_response.json())


if __name__ == '__main__':
    main()
