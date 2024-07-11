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



# Random test user's data  👇

DEVELOPMENT_USERS_LIST = [
    # Club Admin 👇
    {
        "email": "club_admin@mail.com",
        "password": "123njkQ6**N1q",
        "first_name": "Ivan",
        "second_name": "Pizdalov",
        "birth_date": "1994-05-26",
        "sex": 1
    },
    # 10 players 👇
    {
        "email": "user1@example.com",
        "password": "Password1**A1",
        "first_name": "Alex",
        "second_name": "Smith",
        "birth_date": "1990-02-15",
        "sex": 1
    },
    {
        "email": "user2@example.com",
        "password": "Password2**B2",
        "first_name": "Emma",
        "second_name": "Johnson",
        "birth_date": "1988-11-21",
        "sex": 0
    },
    {
        "email": "user3@example.com",
        "password": "Password3**C3",
        "first_name": "Michael",
        "second_name": "Williams",
        "birth_date": "1992-06-30",
        "sex": 1
    },
    {
        "email": "user4@example.com",
        "password": "Password4**D4",
        "first_name": "Olivia",
        "second_name": "Brown",
        "birth_date": "1995-09-10",
        "sex": 0
    },
    {
        "email": "user5@example.com",
        "password": "Password5**E5",
        "first_name": "Daniel",
        "second_name": "Jones",
        "birth_date": "1985-04-19",
        "sex": 1
    },
    {
        "email": "user6@example.com",
        "password": "Password6**F6",
        "first_name": "Sophia",
        "second_name": "Garcia",
        "birth_date": "1993-07-25",
        "sex": 0
    },
    {
        "email": "user7@example.com",
        "password": "Password7**G7",
        "first_name": "David",
        "second_name": "Martinez",
        "birth_date": "1991-12-14",
        "sex": 1
    },
    {
        "email": "user8@example.com",
        "password": "Password8**H8",
        "first_name": "Ava",
        "second_name": "Davis",
        "birth_date": "1989-03-07",
        "sex": 0
    },
    {
        "email": "user9@example.com",
        "password": "Password9**I9",
        "first_name": "James",
        "second_name": "Rodriguez",
        "birth_date": "1994-08-22",
        "sex": 1
    },
    {
        "email": "user10@example.com",
        "password": "Password10**J10",
        "first_name": "Isabella",
        "second_name": "Lopez",
        "birth_date": "1996-01-05",
        "sex": 0
    }
]

DEVELOPMENT_CLUB = {
    "name": "PussyGayClub",
    "state": "Russia",
    "city": "Saint-AbuDabi",
    "address": "Chkalova 37",
    "phone_number": "+79992370953",
    "about": "We love Penis! We hate Tennis!",
    "social_link": "https://instagram.com/table_pennis",
    "link": "https://welovechildrens.com/",
    "opening_hours": {
        "MONDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "TUESDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "WEDNESDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "THURSDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "FRIDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "SATURDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        },
        "SUNDAY": {
            "START": "10:30",
            "FINISH": "21:00"
        }
    }
}

DEVELOPMENT_TOURNAMENT = {
  "name": "Men Fusk Mens - it's real sport!",
  "date_time": "2024-07-03T22:14:00+04:00",
  "club": 1
}