# Python imports
import asyncio

# Django imports
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# import models
from django.contrib.auth.models import User

# import custom foos, classes
from user.services import hashing

User = get_user_model()


class CustomAuthenication(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Overrides the authenticate method to allow users to log in using their email address.
        """
        # NOTE: admin panel send email as username
        if username:
            email = username

        else:
            email = kwargs.get("email")

        try:
            user = User.objects.get(email=email)
            hashed_password = asyncio.run(
                hashing(
                    password
                )
            )

            if hashed_password == user.password:

                return user

            return None

        except User.DoesNotExist as ex:
            # FIXME
            print(ex)

            return None