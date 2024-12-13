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
from user.constants import (
    PASSWORD_IS_REQUIRED,
    EMAIL_IS_REQUIRED,
    GenderChoise,
    GeoChoiсe
)

# import models
from user.models.player import Player

# import custom foos, classes
from user.services import hashing
from main.utils import (
    define_image_file_path
)


def define_user_photo_path(instance, filename):

    return define_image_file_path(
        instance_indicator=str(instance.id),
        filename=filename,
        object_type="_user_photo.",
        directory="user_photoes/"
    )


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
        birth_date = str(os.getenv("SUPER_BIRTH_DATE"))
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        password = os.getenv("SUPER_PASSWORD")
        kwargs.setdefault("email", os.getenv("SUPER_EMAIL"))
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("first_name", os.getenv("SUPER_FIRST_NAME"))
        kwargs.setdefault("second_name", os.getenv("SUPER_SECOND_NAME"))
        kwargs.setdefault("first_name", os.getenv("SUPER_FIRST_NAME"))
        kwargs.setdefault("sex", 0)
        kwargs.setdefault("birth_date", birth_date)

        return self.create_user(password, **kwargs)


class User(AbstractUser):
    '''
    Base model for user. 
    Info about players, club's owners
    are separated in other models.

    User models fields are required fields
    for registrations. Player's fields e.g.
    are not required. 
    '''
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    last_login = last_name = date_joined = username = None

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

    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="User's birth date",
        help_text="User's birth date"
    )

    sex = models.IntegerField(
        choices=GenderChoise,
        null=False,
        help_text="Choise of player's sex"
    )

    # rename default "last name"
    second_name = models.CharField(
        null=False,
        max_length=128,
        verbose_name="User's second name",
        help_text="User's second name"
    )
    geo = models.IntegerField(
        choices=GeoChoiсe,
        null=True,
        verbose_name="User's geo",
        help_text="User can choose 1 from 4 variants"
    )

    @property
    def get_rating(self):

        player_obj = Player.objects.filter(user=self).first()

        if player_obj:
            return player_obj.rating

        else:
            # значит не создана роль игрока для юзера
            return "Не создана роль игрока"

    @property
    def full_name(self):

        return f'{self.first_name} {self.second_name}'

    def save(self, *args, **kwargs):
        """ redefine save method """
        super().save(*args, **kwargs)

        if not Player.objects.filter(user=self).exists():
            Player.objects.create(user=self)

        return self

    def __str__(self):
        second_name = self.second_name if self.second_name else "No Last Name"

        return f"{self.first_name} {second_name} | Email: {self.email}"

    def return_full_name(self):
        second_name = self.second_name if self.second_name else " "

        return f"{second_name} {self.first_name}"

    def __repr__(self):
        return f"email: {self.email}"

