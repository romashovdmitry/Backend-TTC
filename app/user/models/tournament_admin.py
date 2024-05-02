# Django imports
from django.db import models

# import constants
from user.constants import GENDER_CHOISE, HAND_CHOISE


class TournamentAdmin(models.Model):
    """
    Model for admin of Tournament. It could be just manager
    of Tournament or owner of club. 
    """

    class Meta:
        verbose_name = "Tournament Admin"
        verbose_name_plural = "Tournament Admins"
        db_table = "tournament_admin"
        ordering = ['-created']

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

    tournaments_done = models.PositiveIntegerField(
        default=0,
        null=False,
        verbose_name="Tournaments done",
        help_text="Anount of held competitions"
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
