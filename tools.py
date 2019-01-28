"""
Defines standalone functions used within the app.
"""

import binascii
import hashlib
import secrets
import smtplib
import socket
import ssl
import time
from email.message import EmailMessage

import const


def send_verification_email(recipient: str, message: str) -> bool:
    """
    This command performs an entire mail transaction, sending
    the specified `message` to the specified `recipient`.
    """
    try:
        server = smtplib.SMTP(const.SMTP_SERVER, const.SMTP_PORT)
        server.starttls(context=ssl.create_default_context())
        server.login(const.MAILER_ADDR, const.PASSWORD)

        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = const.VERIFY_EMAIL_SUBJECT
        msg['From'] = const.MAILER_ADDR
        msg['To'] = recipient

        sent = server.send_message(msg)
        server.quit()
        return sent
    except Exception as e:
        print(e)
        return False


def hash_password(password: str) -> tuple:
    """
    Hash a password for storing. `pbkdf2_hmac` fits our purposes well.
    It's powerful and available in python3's standard library.
    https://en.wikipedia.org/wiki/PBKDF2
    """
    salt = secrets.token_hex(8)
    pwd_hash = hashlib.pbkdf2_hmac(
        const.HASHING_ALGORITHM,
        password.encode('utf-8'),
        salt.encode('ascii'),
        const.HASHING_ITERATIONS
    )
    pwd_hash = binascii.hexlify(pwd_hash)
    return pwd_hash.decode('ascii'), salt


def verify_password(salt: str, hashing_algorithm: str, stored_password: str, provided_password: str) -> bool:
    """Verify a stored password against the provided password"""
    password_hash = hashlib.pbkdf2_hmac(
        hashing_algorithm,
        provided_password.encode('utf-8'),
        salt.encode('ascii'),
        const.HASHING_ITERATIONS
    )
    password_hash = binascii.hexlify(password_hash).decode('ascii')
    return password_hash == stored_password


def get_free_port() -> int:
    """Returns default port if available, otherwise any available port"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s.connect_ex(('localhost', const.DEFAULT_PORT)) == 0:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        return port
    return const.DEFAULT_PORT


def wait_for_sigint() -> None:
    """Loop until user preses CONTROL-C"""
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        return
