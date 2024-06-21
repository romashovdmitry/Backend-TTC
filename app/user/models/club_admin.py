# import basemodel and django.db.models
from main.base_model import models, BaseModel

# Python imports
import random
import asyncio

# Django imports
from django.db import models

# import custom foos, classes
from user.utils import create_random_code


class ClubAdmin(BaseModel):
    """
    Model for admin of Club. It could be just manager
    of Club or owner of club.
    """

    class Meta:
        verbose_name = "Club Admin"
        verbose_name_plural = "Club Admins"
        db_table = "club_admin"


    enter_code = models.CharField(
        max_length=6,
        null=True,
        verbose_name="Code for authorization in club",
        help_text="New club admin have to enter this code to authorize"
    )

    user = models.ForeignKey(
        "user.user",
        null=True,
        on_delete=models.CASCADE,
        related_name="club_admin_user"
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

    def save(self, *args, **kwargs) -> None:
        """ redefine save method for creating enter_code """
        # if it's first save, that is create
        if not self.id:
            self.enter_code = asyncio.run(create_random_code()) 

        super().save(*args, **kwargs)