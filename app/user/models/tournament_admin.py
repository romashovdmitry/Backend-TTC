# Python imports
import asyncio
from typing import Iterable

# import basemodel and django.db.models
from main.base_model import models, BaseModel

# import constants
from user.constants import GenderChoise

# import custom foos, classes
from user.utils import create_random_code


class TournamentAdmin(BaseModel):
    """
    Model for admin of Tournament. It could be just manager
    of Tournament or owner of club.
    """

    class Meta:
        verbose_name = "Tournament Admin"
        verbose_name_plural = "Tournament Admins"
        db_table = "tournament_admin"

    tournaments_done = models.BooleanField(
        default=False,
        null=False,
        verbose_name="Tournaments done",
        help_text="Anount of held competitions"
    )

    enter_code = models.CharField(
        max_length=6,
        null=True,
        editable=False,
        blank=True,
        verbose_name="Code for authorization in club",
        help_text="New club admin have to enter this code to authorize"
    )

    user = models.ForeignKey(
        "user.user",
        null=True,
        on_delete=models.CASCADE,
        related_name="tournament_admin_user"
    )

    def save(self, *args, **kwargs) -> None:
        """ redefine save method for creating enter_code """
        # if it's first save, that is create
        if not self.id:
            self.enter_code = asyncio.run(create_random_code()) 

        super().save(*args, **kwargs)

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
