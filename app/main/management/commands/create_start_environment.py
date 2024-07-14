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
    DEVELOPMENT_USER_PLAYER_LIST,
    DEVELOPMENT_TOURNAMENT,
    DEVELOPMENT_CLUB,
)

# import custom foos, classes
from user.services import hashing

# .env libs Турнир создан.
import os
from dotenv import load_dotenv
load_dotenv()


# NOTE: it has space for upgrades. But it's for local development.
# so, not very carry about that.

class Command(BaseCommand):
    """ autocreate admin user """
    def handle(self, *args, **options):

        fake_users_list = []
        fake_players_list = []

        for fake_user in DEVELOPMENT_USER_PLAYER_LIST:
            fake_user["user"]["password"] = asyncio.run(
                hashing(fake_user["user"]["password"])
            )

            if not User.objects.filter(email=fake_user["user"]["email"]).exists():
                fake_user_database_object = User.objects.create(
                    **fake_user["user"]
                )
                fake_users_list.append(fake_user_database_object)
                player = Player.objects.filter(
                    user=fake_user_database_object
                ).update(
                    **fake_user["player"]
                )
                
                fake_players_list.append(
                    Player.objects.filter(user=fake_user_database_object).first()
                )

            else:
                fake_user_database_object = User.objects.get(email=fake_user["user"]["email"])
                fake_users_list.append(
                    User.objects.filter(email=fake_user["user"]["email"]).first()
                )
                fake_players_list.append(
                    Player.objects.filter(
                        user=User.objects.filter(
                            email=fake_user["user"]["email"]
                        ).first()
                    ).first()
                )
                self.stdout.write(
                    "Уже создан пользователь "
                    f"{fake_user_database_object.second_name}"
                )

        self.stdout.write("Пользователи созданы.")
        self.stdout.write("Игроки тоже.")

        fake_club_admin = User.objects.get(
            email=DEVELOPMENT_USER_PLAYER_LIST[0]["user"]["email"]
        )

        self.stdout.write("Владелец клуба выбран.")

        if not ClubAdmin.objects.filter(user=fake_club_admin).exists():
            fake_club_admin = ClubAdmin.objects.create(
                user=fake_club_admin
            )

            self.stdout.write("Админ клуба установлен.")

        else:
            fake_club_admin = ClubAdmin.objects.get(
                user=fake_club_admin
            )
            self.stdout.write("Админ клуба уже установлен.")

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
            fake_tournament = Tournament.objects.create(
                **DEVELOPMENT_TOURNAMENT
            )

            self.stdout.write("Турнир создан. ")
        
        else:
            fake_tournament = Tournament.objects.get(
                name=DEVELOPMENT_TOURNAMENT["name"]
            )
            self.stdout.write("Турнир уже создан ранее. ")

        for fake_player in fake_players_list:
        
            if TournamentPlayers.objects.filter(player=fake_player).exists():
                self.stdout.write(
                    f"Игрок {fake_player.user.second_name} уже добавлен на турнир."
                )

            else:
                TournamentPlayers.objects.create(
                    player=fake_player,
                    tournament=fake_tournament
                )
                self.stdout.write(
                    f"Игрока {fake_player.user.second_name} добавили на турнир"
                )