""" create model objects for work on local to imitate real club's usage """
# Python imports
import random

# Django import
from django.core.management.base import BaseCommand

# import models
from tournament.models import Game


class Command(BaseCommand):
    """ autocreate admin user """
    def handle(self, *args, **options):
        all_games = Game.objects.all()
        
        for game in all_games:
            first_score = random.randint(0, 3)

            if first_score == 3:
                second_score = random.randint(0, 2)

            else:
                second_score = 3

            game.first_player_score = first_score
            game.second_player_score = second_score
            game.save()
            self.stdout.write(
                f"Для игры #{game.pk} выставлен счет -> {first_score}:{second_score} "
            )

