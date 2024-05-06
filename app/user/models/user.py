# Python imports
from django.contrib.auth.validators import UnicodeUsernameValidator
from datetime import datetime, timedelta
import pytz
import os
import asyncio

# Django imports
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

# import constants
from user.constants import PASSWORD_IS_REQUIRED, EMAIL_IS_REQUIRED

# import custom foos, classes
from user.services import hashing


class CustomUserManager(BaseUserManager):
    """ Custom class for working with User model """

    def create_user(self, password=None, **kwargs):
        """ custom creating user, using custom hash methods """
        email = kwargs.get("email")

        if not email:
            raise ValueError(EMAIL_IS_REQUIRED)

        if not password:
            raise ValueError(PASSWORD_IS_REQUIRED)

        user = self.model(**kwargs)
        user.email = self.normalize_email(kwargs["email"])
        # Хешируем пароль
        user.password = asyncio.run(
            hashing(
                password=password
            )
        )
        user.save(using=self._db)

        return user

    def create_superuser(self, password=None, **kwargs):
        """ custom creating superuser """
        password = os.getenv("SUPER_PASSWORD")
        kwargs.setdefault("email", os.getenv("SUPER_EMAIL"))
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        return self.create_user(password, **kwargs)


class User(AbstractUser):
    '''
    Base model for user. 
    Info about players, club's owners
    are separated in other models.
    '''
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    last_login = date_joined = username = None

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"
        ordering = ['-created']
        indexes = [
            models.Index(fields=['email'], name='email_index')
            ]

    email = models.EmailField(
        null=True,
        unique=True,
        verbose_name="User's email",
        validators=[EmailValidator],
        error_messages={"unique": "Email exists"}
    )

    password = models.CharField(
        max_length=4096,  # so long because of using custom hashing password
        null=True,
        blank=True,
        verbose_name="User's password",
        help_text="User's password"
    )

    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        help_text="Created date, time"
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text="Update date, time",
        verbose_name=""
    )

    def __str__(self):
        last_name = self.last_name if self.last_name else "No Last Name"
        return f"Email: {self.email}, Last Name: {last_name}"

    def __repr__(self):
        return f"email: {self.email}"

