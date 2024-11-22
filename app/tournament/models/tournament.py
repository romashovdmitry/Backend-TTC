# import basemodel and django.db.models
from main.base_model import models, BaseModel

# import constants
from tournament.constants import (
    TournamentStatus,
    TournamentType,
    DEFAULT_GROUP_QUALIFIRES_NUMBER,
    DEFAULT_MAX_RATING_LIMIT,
    DEFAULT_MIN_RATING_LIMIT
)

# FIXME: это можно без импорта сделать
from club.models.club import Club


class Tournament(BaseModel):
    """
    Tournament model.
    Core model for club, admin.
    We can have club without tournament, but
    tournament must have club and admin.
    """

    class Meta:
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"
        db_table = "tournaments"

    name = models.CharField(
        max_length=128,
        null=True
    )

    date_time = models.DateTimeField(
        null=True,
        verbose_name="Date and Time of Tournament",
        help_text="Date and Time of Tournament",
    )

    type = models.PositiveSmallIntegerField(
        choices=TournamentType,
        default=0,
        verbose_name="Tournament Type",
        help_text="Tournament Type"
    )

    group_number = models.PositiveSmallIntegerField(
        null=True,
        verbose_name="Number of groups in tournament",
        help_text="Number of groups in tournament"
    )

    group_players_number = models.PositiveSmallIntegerField(
        null=True,
        verbose_name="Number of players in one group",
        help_text="Number of players in one group",
    )

    group_qualifiers_number = models.PositiveSmallIntegerField(
        default=DEFAULT_GROUP_QUALIFIRES_NUMBER,
        verbose_name="Number of players who successfully left the group",
        help_text="Number of players who successfully left the group",
    )

    status = models.CharField(
        choices=TournamentStatus,
        max_length=16,
        default=0,
        null=True,
        verbose_name="Tournament Status",
        help_text="Created, started, running or finished. "
    )

    club = models.ForeignKey(
        # FIXME: можно без импорта сделать
        Club,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Club where tournament run",
        help_text="Club where tournament run",
        related_name="club_tournaments"
    )

    tournament_admin = models.ForeignKey(
        "user.TournamentAdmin",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Tournament Admin",
        help_text="Tournament Admin",
        related_name="tournament_admin"
    )

    player_pyament = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Participation payment",
        help_text="Player pay for participation in tournament",
    )
    # NOTE: now we don't use those fiels, but in
    # future maybe would
    min_rating_limit = models.PositiveBigIntegerField(
        default=DEFAULT_MIN_RATING_LIMIT,
        null=False,
        verbose_name="Minimal rating value for players",
        help_text=(
            "Players riched limit could be registrated."
        )
    )
    # NOTE: now we don't use those fiels, but in
    max_rating_limit = models.PositiveBigIntegerField(
        default=DEFAULT_MAX_RATING_LIMIT,
        null=False,
        verbose_name="Maximal rating value for players",
        help_text=(
            "Players riched limit could not be registrated."
        )
    )
