# import basemodel and django.db.models
from main.base_model import models, BaseModel

# import constants
from user.constants import GENDER_CHOISE, HAND_CHOISE


class Player(BaseModel):
    """
    Model for player
    """

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        db_table = "players"

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

    blade = models.CharField(
        max_length=256,
        null=True,
        help_text="Player's Blade"
    )

    rubber_forehand = models.CharField(
        max_length=256,
        null=True,
        help_text="Player's Ruber Forehand"
    )

    rubber_backhand = models.CharField(
        max_length=256,
        null=True,
        help_text="Player's Ruber Backhand"
    )

    user = models.ForeignKey(
        "user.user",
        null=True,
        on_delete=models.CASCADE,
        related_name="player_user"
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