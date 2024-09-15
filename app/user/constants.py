"""
constant data for user app foos, models, services
"""
from django.db import models
from main.settings import MEDIA_ROOT

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


# JSON format that is preffered for frontent-developer Vadim
GET_INFO_ABOUT_USER_RETURN_DICT = {
  "id": None,
  "info": {
    "first_name": None,  # string
    "second_name": None,  # string
    "email": None,  # string
    "birthday": None,  # string
    "avatar": None,  # URL string
  },
  "community": {
    "city": "",
    "playing_hand": None,  # 0 => left; 1 => right
    "racket": {
      "blade": "",
      "rubber_forehand": "",
      "rubber_backhand": "",
    }
  },
  "rating": {
    "dates": ["25.3.2022", "27.2.2021", "10.1.2021", "11.10.2021", "18.7.2023", "23.9.2021", "26.12.2020", "8.8.2022", "4.5.2020", "4.10.2022", "24.5.2023", "29.11.2020", "29.2.2021", "16.10.2020", "19.3.2021", "16.11.2022", "15.3.2022", "22.5.2021", "14.7.2021", "22.8.2021", "19.7.2024", "14.5.2024", "8.2.2021", "10.2.2021", "8.6.2020" ],
    "data": [5, 4, 6, 23, 2, 17, 5, 2, 11, 26, 10, 21, 17, 8, 19, 29, 13, 9, 11, 5, 19, 30, 8, 22, 9 ]
  }
}.copy()

GeoChoise = [
    (1, 'Dubai'),
    (2, 'Abu-Dhabi'),
    (3, 'Sharjah'),
    (4, 'Other Emirate'),
]

DEFAULT_USER_PHOTO_PATH = MEDIA_ROOT + "/defaults/player_photo.png"