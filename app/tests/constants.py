"""
declaring different scenarious for tests and static data for tests
"""
# default created user
DEFAULT_EMAIL = "test_test@mail.com"
DEFAULT_USERNAME = "testTEst1234"
DEFAULT_PASSWORD = "asdnjk123!nNNNj!11"

# default correct fields for testing user scenarious
CORRECT_EMAIL = "AbasdnjjQ!7816@gmail.com"
CORRECT_USERNAME = "Abukidasnkdlasndj"
CORRECT_PASSWORD = "qweASD123"

# wrong email data
WRONG_EMAILS = [
    "romashov",
    "123123123",
    "romashov@ru"
]

# wrong password data
NO_DIGIT_PASSWORD = "SSSSnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn"
TOO_LONG_PASSWORD = "AAAAAAAAAAAAAAaaaaaaaaaa123"
TOO_SHORT_PASSWORD = "1Bhd!"
LOWERCASE_PASSWORD = "nnnn123nnnnnnnn"

# wrong username data

# email errors
WRONG_EMAIL_JSON = {'email': ['Enter a valid email address.']}
EMAIL_EXISTS_JSON = {'email': ['email already exists']}

# username errors
USERNAME_ALREADY_EXISTS_ERROR = {"username": ["Username already exists"]}

# password errors
TOO_SHORT_PASSWORD_ERROR_JSON = {"password": ["Password must be at least 7 characters long."]}
TOO_LONG_PASSWORD_ERROR_JSON = {"password": ["Password must be at most 20 characters long."]}
UPPERCASE_PASSWORD_ERROR_JSON = {'password': ['Password must contain at least one uppercase letter.']}
NO_DIGITS_PASSWORD_ERROR_JSON = {'password': ['Password must contain at least one digit.']}

CREATE_USER_SCENARIOUS = [
    # wrong email scenarious
    {
        "wrong_raw": {
            "name": "email",
            "data": WRONG_EMAILS
    },
        "error_json": WRONG_EMAIL_JSON
    },
    {
        "wrong_raw": {
            "name": "email",
            "data": [DEFAULT_EMAIL]
        },
        "error_json": EMAIL_EXISTS_JSON
    },
    # wrong password scenarious
    {
        "wrong_raw": {
            "name": "password",
            "data": [NO_DIGIT_PASSWORD]
        },
        "error_json": NO_DIGITS_PASSWORD_ERROR_JSON
    },
    {
        "wrong_raw": {
            "name": "password",
            "data": [TOO_LONG_PASSWORD]
        },
        "error_json": TOO_LONG_PASSWORD_ERROR_JSON
    },
    {
        "wrong_raw": {
            "name": "password",
            "data": [LOWERCASE_PASSWORD]
        },
        "error_json": UPPERCASE_PASSWORD_ERROR_JSON
    },
    {
        "wrong_raw": {
            "name": "password",
            "data": [TOO_SHORT_PASSWORD]
        },
        "error_json": TOO_SHORT_PASSWORD_ERROR_JSON
    },
    # wrong username scenarious
    {
        "wrong_raw": {
            "name": "username",
            "data": [DEFAULT_USERNAME]
        },
        "error_json": USERNAME_ALREADY_EXISTS_ERROR
    }
]

