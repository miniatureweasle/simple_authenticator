"""
Defines database operations for the app
The connection handler decorator allows us to forget about opening
and closing connections (forget about conn=None for the most part)

Usage:

@connection_handler
def setup(conn=None)
    ...
    return True

setup() <- this will run with default DB_FILE defined in const.py
"""

import sqlite3
from typing import Optional, Callable, Any

import const


def connect(db_file) -> Optional[sqlite3.Connection]:
    """Connects to a SQLite3 database specified by `db_file`"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        # TODO: add logging here
        print('Database Error')
        print(e)

    return None


def connection_handler(db_ops_func: Callable[..., Any]) -> Callable[..., Any]:
    """Handles opening and closing connections to the DB"""
    def wrapper_connection_handler(*args, **kwargs):
        conn = connect(const.DB_FILE)
        if conn:
            try:
                result = db_ops_func(*args, conn=conn)
                conn.close()
                return result
            except sqlite3.Error as e:
                # return false for any operation causes an sqlite3 exception
                # TODO: add logging here
                print('Database Error')
                print(e)
                return False
        else:
            # return False to any operation if connection fails
            return False
    return wrapper_connection_handler


@connection_handler
def setup(conn=None) -> bool:
    """Setup the DB"""
    sql = ('CREATE TABLE IF NOT EXISTS user_states'
           '( id INTEGER PRIMARY KEY AUTOINCREMENT,'
           '  name TEXT'
           ')'
          )
    conn.execute(sql)
    sql = ('INSERT OR REPLACE INTO user_states '
           'VALUES (2, "EMAIL_UNVERIFIED");'
          )
    sql = sql.format(const.STATE_EMAIL_UNVERIFIED_ID)
    conn.execute(sql)
    sql = ('INSERT OR REPLACE INTO user_states '
           'VALUES (1, "EMAIL_VERIFIED")'
          )
    sql = sql.format(const.STATE_EMAIL_VERIFIED_ID)
    conn.execute(sql)
    sql = ('CREATE TABLE IF NOT EXISTS users'
           '(email TEXT PRIMARY KEY,'
           'password TEXT,'
           'password_salt TEXT,'
           'password_hash_algorithm TEXT,'
           'email_verification_token TEXT,'
           'state_id INTEGER,'
           'FOREIGN KEY (state_id) REFERENCES user_states(id))'
          )
    conn.execute(sql)
    conn.commit()
    return True


@connection_handler
def user_exists(email: str, conn=None) -> bool:
    """Check if user with specified `email` exist"""
    sql = ("SELECT EXISTS("
           "SELECT 1 FROM users WHERE email='{}')"
           )
    sql = sql.format(email)
    does_exist = conn.cursor().execute(sql).fetchall()[0][0]
    return does_exist


@connection_handler
def create_user(user: tuple, conn=None) -> bool:
    """Create a user with the specified `user` details"""
    sql = (
            'INSERT INTO users('
            'email,'
            'password,'
            'password_salt,'
            'password_hash_algorithm,'
            'email_verification_token,'
            'state_id)'
            'VALUES(?,?,?,?,?,?)'
          )
    _ = conn.cursor().execute(sql, user)
    conn.commit()
    return True


@connection_handler
def user_w_token_exists(token, conn=None) -> bool:
    """Checks if a user with the specified `token` exists"""
    sql = "SELECT EXISTS(SELECT 1 FROM users WHERE email_verification_token='{}')"
    sql = sql.format(token)
    does_exist = conn.cursor().execute(sql).fetchall()[0][0]
    return does_exist


@connection_handler
def verify_user(token, conn=None) -> bool:
    """
    Verifies a user by removing their email verification token and
    setting their state to verified.
    """
    sql = ("UPDATE users "
           "SET email_verification_token=null,"
           "state_id={} "
           "WHERE email_verification_token='{}'"
     )
    sql = sql.format(const.STATE_EMAIL_VERIFIED_ID, token)
    _ = conn.cursor().execute(sql)
    conn.commit()
    return True


@connection_handler
def email_is_verified(email, conn=None) -> bool:
    """Checks if an email is verified"""
    sql = ("SELECT EXISTS "
           "(SELECT 1 FROM users WHERE email='{}' "
           "AND email_verification_token is null "
           "AND state_id=2)"
           )
    sql = sql.format(email)
    email_verified = conn.cursor().execute(sql).fetchall()[0][0]
    return email_verified


@connection_handler
def get_password_details(email, conn=None) -> tuple:
    """Get the password details for the specified `email`"""
    sql = ("SELECT "
           "password,"
           "password_salt,"
           "password_hash_algorithm "
           "FROM users "
           "WHERE email='{}'"
           )
    sql = sql.format(email)
    password_details = conn.cursor().execute(sql).fetchall()[0]
    return password_details
