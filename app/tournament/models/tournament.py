# Django imports
from django.db import models

# import constants
from tournament.constants import TOURNAMENT_STATUS


class Tournament(models.Model):
    """
    Tournament model.
    Core model for club, admin.
    We can have club without tournament, but
    tournament must have club and admin.
    """
    name = models.CharField(
        max_length=128,
        null=True
    )

    date_time = models.DateTimeField(
        null=True,
        verbose_name="Date and Time of Tournament",
        help_text="Date and Time of Tournament",
    )

    max_players_amount = models.PositiveSmallIntegerField(
        default=16,
        verbose_name="Max amount of players",
        help_text=(
            "Max amount of players, that "
            "could be registrated of tournament"
        )
    )

    min_rating_limit = models.PositiveBigIntegerField(
        default=100,
        null=False,
        verbose_name="Minimal rating value for players",
        help_text=(
            "Players riched limit could be registrated."
        )
    )

    max_rating_limit = models.PositiveBigIntegerField(
        default=1000,
        null=False,
        verbose_name="Maximal rating value for players",
        help_text=(
            "Players riched limit could not be registrated."
        )
    )

    status = models.CharField(
        choices=TOURNAMENT_STATUS,
        null=True,
        verbose_name="Tournament Status",
        help_text="Created, started, running or finished. "
    )

    club = models.ForeignKey(
        "club.club",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Club where tournament run",
        help_text="Club where tournament run"
    )

    tournament_admin = models.ForeignKey(
        "user.TournamentAdmin",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Tournament Admin",
        help_text="Tournament Admin"
    )
