# Django imports
from django.db import models

# import constants
from user.constants import GENDER_CHOISE, HAND_CHOISE


class Player(models.Model):
    """
    Model for player
    """

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        db_table = "players"
        ordering = ['-created']

    sex = models.CharField(
        choices=GENDER_CHOISE,
        null=True,
        help_text="Choise of player's sex"
    )

    handedness = models.CharField(
        choices=HAND_CHOISE,
        null=True,
        help_text="By which hand player prefer to play, or both"
    )

    rating = models.PositiveBigIntegerField(
        default=100,
        null=False,
        help_text="Rating of player in club rating system"
    )

    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        help_text="Created date, time"
    )
    updated = models.DateTimeField(
        auto_now=True,
        help_text="Update date, time",
        verbose_name=""
    )

    user = models.ForeignKey(
        "user.user",
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"First name: {self.user.first_name}, "
            f"Last name: {self.user.last_name}"
        )

    def __repr__(self):
        return (
            f"ID: {self.id}, "
            f"First name: {self.user.first_name}, "
            f"Last name: {self.user.last_name}"
        )