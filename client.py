import argparse

import requests

import const
import tools
from runserver import SimpleHTTPSServer


def login(user_email, user_password, server_port):
    """Logs in a user"""
    payload = {'email': user_email, 'password': user_password}
    url = 'https://localhost:{}/login'.format(server_port)
    response = requests.post(url, data=payload, verify='./ssl/self-signed.crt')
    print(str(response.content))


def signup(user_email, user_password, server_port):
    """Signs up a user"""
    payload = {'email': user_email, 'password': user_password}
    url = 'https://localhost:{}/signup'.format(server_port)
    response = requests.post(url, data=payload, verify='./ssl/self-signed.crt')
    response_content = str(response.content)
    print(response_content)
    if 'Success' in response_content:
        print("Don't shutdown server until email verification link is clicked!")
        print('Shutdown with CTRL-C')
        tools.wait_for_sigint()


def verify(email_verification_token, server_port):
    """Verifies a user"""
    url = 'https://localhost:{}/verify?token={}'.format(server_port, email_verification_token)
    # ensure our self-signed certificate is trusted
    response = requests.get(url, verify='./ssl/self-signed.crt')
    print(response.content)


def prompt_cred() -> tuple:
    user_email = input('Enter email:\n')
    user_password = input('Enter password:\n')
    return user_email, user_password


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'endpoint',
        choices=['signup', 'login', 'verify'],
        help='signup, verify, login'
    )
    args = parser.parse_args()

    print(const.APP_NAME)
    server = SimpleHTTPSServer()

    if args.endpoint == 'signup':
        print('Signup Selected')
        email, password = prompt_cred()
        signup(email, password, server.port)
    elif args.endpoint == 'login':
        print('Login Selected')
        email, password = prompt_cred()
        login(email, password, server.port)
    elif args.endpoint == 'verify':
        print('Verify Selected')
        token = input('Enter token\n')
        verify(token, server.port)
    else:
        print('Invalid argument. enter "signup" or "login"')
