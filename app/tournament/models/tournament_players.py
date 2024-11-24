# import basemodel and django.db.models
from main.base_model import models, BaseModel

# import models
from tournament.models import Tournament
from user.models import Player
from club.models.club import Club

# import constants
from tournament.constants import TournamentStage


class TournamentPlayers(BaseModel):
    """
    Model where we save info
    about players that was added by club admin
    to tournament.
    """
    class Meta:
        verbose_name = "Tournament Player"
        verbose_name_plural = "Tournament Players"
        db_table = "tournament_players"
        unique_together = ("tournament", "player")

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="tournament_players",
        verbose_name="Проводимый клубом туринр.",
        help_text="Проводимый клубом туринр."
    )

    player = models.ForeignKey(
        Player,
        verbose_name="Участник турнира",
        help_text="Участник турнира",
        on_delete=models.CASCADE
    )
    tournament_group = models.PositiveSmallIntegerField(
        null=True,
        verbose_name="Группа игрока на турнире",
        help_text="Группа игрока на турнире"
    )
    stage = models.PositiveSmallIntegerField(
        choices=TournamentStage,
        null=True,
        verbose_name="Этап, на котором находится игрок в рамках турнира. ",
        help_text="Этап, на котором находится игрок в рамках турнира. "
    )
    points = models.PositiveSmallIntegerField(
        null=True,
        default=0,
        verbose_name="Очки игрока в рамках текущего этапа турнира",
        help_text="Очки игрока в рамках текущего этапа турнира"
    )
