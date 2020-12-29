"""
This is a command-line application which displays all entry titles associated
with an author inputted by the user.
"""

import requests

API_BASE_URL = 'http://127.0.0.1:5000/'


def main():
    request_url = '{}/entries'.format(API_BASE_URL)
    response = requests.get(request_url)
    content = response.json()

    requested_author = input('Enter an author name: ')

    print('Here are the entry titles associated with the author:')
    for result in content:
        if result['author'] == requested_author:
            print(result['title'])


if __name__ == '__main__':
    main()
