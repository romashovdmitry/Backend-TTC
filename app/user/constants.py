"""
constant data for user app foos, models, services
"""
from django.db import models

# error messages
PASSWORD_IS_REQUIRED = "Password is required for new user"
EMAIL_IS_REQUIRED = "User must have any email for registrations"


class HandChoise(models.IntegerChoices):

    RIGHT_HAND = 0, 'RIGHT_HAND'
    LEFT_HAND = 1, 'LEFT_HAND'
    BOTH = 2, 'BOTH'


class GenderChoise(models.IntegerChoices):

    MALE = 0, 'MALE'
    FEMALE = 1, 'FEMALE'