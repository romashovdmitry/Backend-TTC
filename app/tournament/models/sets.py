# import basemodel and django.db.models
from main.base_model import models


class Set(models.Model):
    """
    Class for saving tournament's Games.
    """
    class Meta:
        db_table = "sets"
        verbose_name = "Set"
        verbose_name_plural = "Sets"

    first_player_points = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Another one player of game",
        help_text="Another one player of game"
    )
    second_player_points = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Another one player of game",
        help_text="Another one player of game"
    )
