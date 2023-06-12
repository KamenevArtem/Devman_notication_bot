import os
import requests

from dotenv import load_dotenv


def get_user_reviews(headers):
    url = 'https://dvmn.org/api/user_reviews/'
    reviews_response = requests.get(url, headers=headers)
    reviews_response.raise_for_status()
    return reviews_response.json()


def long_polling_reviews(headers):
    url = 'https://dvmn.org/api/long_polling/'
    long_polling_response = requests.get(
        url,
        headers=headers,
    )
    long_polling_response.raise_for_status()
    response = long_polling_response.json()
    if 'timestamp_to_request' in response:
        params = {
            'timestamp': {response['timestamp_to_request']}
        }
        timestamp_response = requests.get(
            url,
            headers=headers,
            params=params
        )
        timestamp_response.raise_for_status()
        return timestamp_response.json()
    else:
        return long_polling_response.json()


def main():
    load_dotenv()
    access_token = os.environ['DEVMAN_API_TOKEN']
    headers = {
        'Authorization': f'Token {access_token}'
    }
    get_user_reviews(headers)
    while True:
        try:
            long_polling_reviews(headers)
        except (requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError):
            pass


if __name__ == '__main__':
    main()
