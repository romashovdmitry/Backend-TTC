""" create model objects for work on local to imitate real club's usage """
# Python imports
import asyncio

# Django import
from django.core.management.base import BaseCommand

# import models
from user.models import (
    User,
    Player,
    ClubAdmin
)
from club.models import (
    Club
)
from tournament.models import (
    Tournament,
    TournamentPlayers
)

# import constants
from user.constants import (
    DEVELOPMENT_USERS_LIST,
    DEVELOPMENT_CLUB
)

# import custom foos, classes
from user.services import hashing

# .env libs import
import os
from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    """ autocreate admin user """
    def handle(self, *args, **options):

        for fake_user in DEVELOPMENT_USERS_LIST:
            fake_user["password"] = asyncio.run(
                hashing(fake_user["password"])
            )
            User.objects.create(
                **fake_user
            )

        self.stdout.write("Пользователи созданы.")

        fake_club_admin = User.objects.get(
            email=DEVELOPMENT_USERS_LIST[0]["email"]
        )

        self.stdout.write("Владелец клуба выбран.")

        fake_club_admin = ClubAdmin.objects.create(
            user=fake_club_admin
        )

        self.stdout.write("Админи клуба установлен.")

        fake_club_object = Club.objects.create(
            **DEVELOPMENT_CLUB
        )

        self.stdout.write("Клуб создан.")

        fake_club_object.admin_club = fake_club_admin
        fake_club_object.save()

        self.stdout.write("Владелец для клуба установлен. ")

        