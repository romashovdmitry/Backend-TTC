# Python imports
from django.db import models

# import models
from user.models import Player


class PlayerRatingHistory(models.Model):
    """
    Dates when rating was changed and new rating
    that was set.
    """
    class Meta:
        db_table = "player_rating_history"
        verbose_name = "Player's rating history"
        verbose_name_plural = "Player's rating history"        

    created = models.DateField(
        blank=True,
        verbose_name="Date,",
        help_text="Created date, time",
        null=True
    )
    actual_rating = models.PositiveIntegerField()
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
