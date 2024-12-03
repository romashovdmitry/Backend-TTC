# Python imports
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz
import hashlib

# Django imports
from rest_framework.response import Response

# JWT imports
from rest_framework_simplejwt.tokens import RefreshToken


load_dotenv()


async def hashing(
        password: str
) -> str:
    """
    Foo hashs password entered by user.

    Parameters:
        password: string enetered by user in
            password field
    Returns:
        str: hashed password
    """

    password_start = os.getenv('PASSWORD_START')
    password_finish = os.getenv('PASSWORD_FINISH')
    HASH_ALGO = os.getenv('CUSTOM_HASH_ALGO')

    password = password_start + password + password_finish
    password = password.encode('utf-8')
    password = hashlib.new(HASH_ALGO, password).hexdigest()
    salt = password[3:6]
    salt = salt.encode('utf-8')
    password = password.encode('utf-8')
    hashed_password = hashlib.pbkdf2_hmac(
            hash_name=HASH_ALGO, password=password, salt=salt, iterations=100000)

    return (hashed_password.hex())


class JWTActions:
    """
    Class for creating JWT and
    set JWY in cookies by response.

    It's better practice to make tokens
    secure, httponly and set it straightaway
    on cookies, either return in JSON-body
    response.
    """

    def __init__(
        self,
        response: Response = None,
        instance=None  # User typing
    ) -> None:
        """
        Attrs initialize
         
        Parameters:
            response: Response that we are
                going to return to user
            instance: obj of user Model,
                that we proccessing
        
        """
        self.response = response
        self.instance = instance
        time_zone = pytz.UTC
        self.now = time_zone.localize(datetime.utcnow())

    async def set_cookies_on_response(self) -> Response:
        """
        Set up cookies on response.

        Returns:
            Response: HttpResponse with jwt-cookies.
        """
        refresh_token = RefreshToken.for_user(self.instance)
        response_data = [
            {
                "cookie_key": "access_token",
                "cookie_value": str(refresh_token.access_token),
                "max_age": int(os.getenv("ACCESS_TOKEN_LIFETIME_IN_SECONDS")),
                # "secure_and_httponly": True,
                "path": "/"
            },
            {
                "cookie_key": "refresh_token",
                "cookie_value": str(refresh_token),
                "max_age": int(os.getenv("REFRESH_TOKEN_LIFETIME_IN_SECONDS")),
                # "secure_and_httponly": True,
                "path": "api/v1/user/"
            },
            {
                "cookie_key": "signed_in",
                "cookie_value": True,
                "max_age": int(os.getenv("REFRESH_TOKEN_LIFETIME_IN_SECONDS")),
                # "secure_and_httponly": True,
                "path": "/"
            }
        ]
        for obj in response_data:
            self.response.set_cookie(
                obj["cookie_key"],
                obj["cookie_value"],
                max_age=obj["max_age"],
                # secure=obj["secure_and_httponly"],
                # httponly=obj["secure_and_httponly"],
                # samesite="None",
                path=obj["path"]
            )
        # for work with Swagger on machine or local
        print(f'refresh_token -> {refresh_token}\n')
        print(f'access_token -> {refresh_token.access_token}')

        return self.response