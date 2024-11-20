# Django imports
from django.dispatch import Signal
from django.db.models.signals import post_save
from django.dispatch import receiver

# import models
from app.tournament.models import Game


# NOTE: пока ничего не делает
@receiver(post_save, sender=Game)
def game_completed_handler(
    sender,
    instance: Game,
    created,
    **kwargs
):
    if created:

        return

    if (
        instance.first_player_score is not None
        and instance.second_player_score is not None
    ):
        print('come here bich')