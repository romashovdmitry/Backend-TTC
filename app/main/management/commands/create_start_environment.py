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
from main.constants import (
    DEVELOPMENT_USERS_LIST,
    DEVELOPMENT_CLUB,
    DEVELOPMENT_TOURNAMENT
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

            if not User.objects.filter(email=fake_user["email"]).exists():
                User.objects.create(
                    **fake_user
                )
            else:
                self.stdout.write(
                    "Уже создан пользователь "
                    f"{fake_user['second_name']}"
                )

        self.stdout.write("Пользователи созданы.")

        fake_club_admin = User.objects.get(
            email=DEVELOPMENT_USERS_LIST[0]["email"]
        )

        self.stdout.write("Владелец клуба выбран.")

        fake_club_admin = ClubAdmin.objects.create(
            user=fake_club_admin
        )

        self.stdout.write("Админ клуба установлен.")

        if not Club.objects.filter(name=DEVELOPMENT_CLUB["name"]).exists():
            fake_club_object = Club.objects.create(
                **DEVELOPMENT_CLUB
            )

            self.stdout.write("Клуб создан.")

        else:
            fake_club_object = Club.objects.get(name=DEVELOPMENT_CLUB["name"])
            self.stdout.write(
                f"Есть уже клуб {DEVELOPMENT_CLUB['name']}"
            )            

        fake_club_object.admin_club = fake_club_admin
        fake_club_object.save()

        self.stdout.write("Владелец для клуба установлен. ")

        DEVELOPMENT_TOURNAMENT["club"] = Club.objects.get(
            pk=DEVELOPMENT_TOURNAMENT["club"]
        )

        if not Tournament.objects.filter(
            name=DEVELOPMENT_TOURNAMENT["name"]
        ).exists():
            Tournament.objects.create(
                DEVELOPMENT_TOURNAMENT
            )

            self.stdout.write("Турнир создан. ")
        
        else:
            self.stdout.write("Турнир уже создан ранее. ")
