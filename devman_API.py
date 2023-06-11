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
    response = requests.get(reviews_url, headers=headers)
    response.raise_for_status()
    pprint(response.json())


if __name__ == '__main__':
    main()
