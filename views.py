import json
import re
import secrets
from urllib.parse import parse_qs

import const
from database import db_ops
import tools


def validate(fields: dict) -> dict:
    """Ensures `fields` conform to the validation rules of the API"""
    errors = {'Errors': []}
    password = fields.get('password', '')
    if 'password' not in fields:
        errors['Errors'].append({'password': const.FIELD_REQUIRED})
    elif not const.PW_MIN <= len(password) <= const.PW_MAX:
        errors['Errors'].append({'password': const.INVALID_PASSWORD})
    if 'email' not in fields:
        errors['Errors'].append({'email': const.FIELD_REQUIRED})
    elif not re.match(const.VALID_EMAIL_PATTERN, fields.get('email', '')):
        errors['Errors'].append({'email': const.INVALID_EMAIL})

    if len(errors.get('Errors')) > 0:
        return errors
    return fields


def signup(environ, start_response) -> bytearray:
    """Signs up a user"""
    validated_data = validate(environ['params'])
    if 'Errors' not in validated_data:
        email = validated_data['email']
        password = validated_data['password']
        if not db_ops.user_exists(email):
            password_hash, password_salt = tools.hash_password(password)
            email_verification_token = secrets.token_hex()
            row = (
                email,
                password_hash,
                password_salt,
                const.HASHING_ALGORITHM,
                email_verification_token,
                const.STATE_EMAIL_UNVERIFIED_ID
            )
            if db_ops.create_user(row):
                link = '{}:{}/verify?token={}'
                link = link.format(const.LOCAL_URL, environ['SERVER_PORT'], email_verification_token)
                verification_msg = const.VERIFY_EMAIL_MSG + link
                tools.send_verification_email(validated_data['email'], verification_msg )

                start_response(const.CREATED_201, const.JSON_HEADERS)
                yield const.SUCCESS
            else:
                # likely database insert failed, check logs (when they exist)
                start_response(const.INTERNAL_SERVER_ERROR_500, const.JSON_HEADERS)
                yield const.INTERNAL_SERVER_ERROR
        else:
            start_response(const.CONFLICT_409, const.JSON_HEADERS)
            yield const.USERNAME_EXISTS
    else:
        validation_errors = json.dumps(validated_data).encode('utf-8')
        start_response(const.BAD_REQUEST_400, const.JSON_HEADERS)
        yield validation_errors


def verify(environ, start_response) -> bytearray:
    """Verifies a users email address"""
    token = parse_qs(environ['QUERY_STRING']).get('token', [''])[0]
    # lets avoid script injection by escaping user input
    token = re.escape(token)
    if db_ops.user_w_token_exists(token):
        db_ops.verify_user(token)
        start_response(const.OK_200, const.TEXT_HEADERS)
        yield const.SUCCESS
    else:
        start_response(const.BAD_REQUEST_400, const.TEXT_HEADERS)
        yield const.NO_USER_WITH_THAT_TOKEN


def login(environ, start_response) -> bytearray:
    """Logs in a user"""
    validated_data = validate(environ['params'])
    if 'Errors' not in validated_data:
        user_email = validated_data['email']

        if db_ops.user_exists(user_email):
            pwd, salt, algorithm = db_ops.get_password_details(user_email)
            if tools.verify_password(salt, algorithm, pwd, validated_data['password']):
                if db_ops.email_is_verified(user_email):
                    start_response(const.OK_200, const.TEXT_HEADERS)
                    yield const.SUCCESS
                else:
                    start_response(const.FORBIDDEN_403, const.TEXT_HEADERS)
                    yield const.EMAIL_UNVERIFIED
            else:
                start_response(const.UNAUTHORIZED_401, const.TEXT_HEADERS)
                yield const.INCORRECT_PASSWORD
        else:
            start_response(const.BAD_REQUEST_400, const.TEXT_HEADERS)
            yield const.USER_DOES_NOT_EXIST
    else:
        validation_errors = json.dumps(validated_data).encode('utf-8')
        start_response(const.BAD_REQUEST_400, const.JSON_HEADERS)
        yield validation_errors
