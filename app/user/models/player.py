# import basemodel and django.db.models
from main.base_model import models, BaseModel

# import constants
from user.constants import HandChoise

# import custom foos, classes
from main.utils import (
    define_image_file_path,
    image_file_extension_validator
)


def define_user_photo_path(instance, filename):

    return define_image_file_path(
        instance_indicator=str(instance.id),
        filename=filename,
        object_type="_user_photo.",
        directory="user_photoes/"
    )


class Player(BaseModel):
    """
    Model for player
    """

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"
        db_table = "players"
        ordering = ['-rating']

    playing_hand = models.IntegerField(
        choices=HandChoise,
        max_length=16,
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
    
    photo = models.ImageField(
        upload_to=define_user_photo_path,
        null=True,
        verbose_name="User Photo",
        help_text="User Photo",
        validators=[image_file_extension_validator]
    )

    def __str__(self):
        return (
            f"ID: {self.id}, "
            f"First name: {self.user.first_name}, "
            f"Last name: {self.user.second_name}"
        )

    def __repr__(self):
        return (
            f"ID: {self.id}, "
            f"First name: {self.user.first_name}, "
            f"Last name: {self.user.second_name}"
        )