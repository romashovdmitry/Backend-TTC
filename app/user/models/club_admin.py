# Python imports
import random

# Django imports
from typing import Iterable
from django.db import models

# import constants
from user.constants import GENDER_CHOISE, HAND_CHOISE


class ClubAdmin(models.Model):
    """
    Model for admin of Club. It could be just manager
    of Club or owner of club.
    """

    class Meta:
        verbose_name = "Club Admin"
        verbose_name_plural = "Club Admins"
        db_table = "club_admin"
        ordering = ['-created']

    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        help_text="Created date, time"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Update date, time",
        help_text="Update date, time"
    )

    user = models.ForeignKey(
        "user.user",
        null=True,
        on_delete=models.CASCADE
    )

    enter_code = models.CharField(
        max_length=6,
        null=True,
        verbose_name="Code for authorization in club",
        help_text="New club admin have to enter this code to authorize"
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

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        random_code = ""

        for _ in range(6):
            random_code += str(random.randint(0, 9))
        self.enter_code = random_code

        return super().save(force_insert, force_update, using, update_fields)