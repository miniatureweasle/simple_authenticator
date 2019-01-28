APP_NAME = 'Plug & Play Authenticator'
DEFAULT_PORT = 8080

# Database Config
DB_FILE = 'database/simple_auth.db'
STATE_EMAIL_UNVERIFIED_ID = 1
STATE_EMAIL_VERIFIED_ID = 2
HASHING_ALGORITHM = 'sha512'
HASHING_ITERATIONS = 1000

# SMTP Config
UNAME = 'whitetestmouse@gmail.com'
PASSWORD = 'testmousequickfox'
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MAILER_ADDR = "whitetestmouse@gmail.com"
VERIFY_EMAIL_SUBJECT = 'Email Verification from {}'.format(APP_NAME)
VERIFY_EMAIL_MSG = "Please click the following link to verify your email address "
LOCAL_URL = 'https://127.0.0.1'

# HTTP Headers And Status Codes
OK_200 = '200 OK'
CREATED_201 = '201 Created'
BAD_REQUEST_400 = '400 Bad Request'
UNAUTHORIZED_401 = '401 Unauthorized'
FORBIDDEN_403 = '403 Forbidden'
CONFLICT_409 = '409 Conflict'
INTERNAL_SERVER_ERROR_500 = '500 Internal Server Error'
JSON_HEADERS = [('Content-type', 'application/json')]
TEXT_HEADERS = [('Content-type', 'text/html')]

# Response Messages
USER_DOES_NOT_EXIST = b'A user with that email not exist.'
USERNAME_EXISTS = b'A user with that email already exists.'
INCORRECT_PASSWORD = b'Password incorrect.'
EMAIL_UNVERIFIED = b'Login failed. User unverified, check your email for a verification link.'
NO_USER_WITH_THAT_TOKEN = b'No user exists with the specified token'
SUCCESS = b'Success'
INTERNAL_SERVER_ERROR = b'Internal Server Error'

# Field Validation
PW_MIN = 5
PW_MAX = 100
VALID_EMAIL_PATTERN = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
INVALID_PASSWORD = "Invalid password length (must be between {} and {}).".format(PW_MIN, PW_MAX)
INVALID_EMAIL = 'Invalid email address (valid example john@gmail.com).'
FIELD_REQUIRED = "This field is required."
