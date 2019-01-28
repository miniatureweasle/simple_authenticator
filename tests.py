"""
Some unit tests for the API. Future tasks could include:

1. more extensive validation testing
2. dry-run email testing
3. testing various user actions

"""
import unittest

import requests

import const
from runserver import SimpleHTTPSServer


class TestAPI(unittest.TestCase):
    server = SimpleHTTPSServer()

    def test_username_required(self):
        payload = {'username': 'test'}
        url = 'https://localhost:{}/signup'.format(TestAPI.server.port)
        # ensure our self-signed certificate is trusted
        response = requests.post(url, data=payload, verify='./ssl/self-signed.crt')
        self.assertTrue('Errors' in response.json())
        username_validation_error = {'email': const.FIELD_REQUIRED}
        self.assertTrue(username_validation_error in response.json()['Errors'])

    def test_password_required(self):
        payload = {'passwrod': 'test'}
        url = 'https://localhost:{}/signup'.format(TestAPI.server.port)
        # ensure our self-signed certificate is trusted
        response = requests.post(url, data=payload, verify='./ssl/self-signed.crt')
        self.assertTrue('Errors' in response.json())
        password_validation_error = {'password': const.FIELD_REQUIRED}
        self.assertTrue(password_validation_error in response.json()['Errors'])

    def test_api_accepts_integer_passwords(self):
        payload = {'password': 33333333}
        url = 'https://localhost:{}/signup'.format(TestAPI.server.port)
        # ensure our self-signed certificate is trusted
        response = requests.post(url, data=payload, verify='./ssl/self-signed.crt')
        self.assertTrue('Errors' in response.json())
        password_validation_error = {'password': const.FIELD_REQUIRED}
        self.assertTrue(password_validation_error not in response.json()['Errors'])

    def test_invalid_email(self):
        payload = {'email': 123}
        url = 'https://localhost:{}/signup'.format(TestAPI.server.port)
        # ensure our self-signed certificate is trusted
        response = requests.post(url, data=payload, verify='./ssl/self-signed.crt')
        self.assertTrue('Errors' in response.json())
        email_validation_error = {'email': const.INVALID_EMAIL}
        self.assertTrue(email_validation_error in response.json()['Errors'])

    def test_invalid_token(self):
        url = 'https://localhost:{}/verify?token=1234'.format(TestAPI.server.port)
        # ensure our self-signed certificate is trusted
        response = requests.get(url, verify='./ssl/self-signed.crt')
        self.assertTrue(const.NO_USER_WITH_THAT_TOKEN in response.content)

if __name__ == '__main__':
    unittest.main()
