# import basemodel and django.db.models
from main.base_model import models, BaseModel

# import models
from tournament.models import Tournament
from user.models import Player

# import models
from club.models.club import Club


class TournamentPlayers(BaseModel):
    """
    Model where we save info
    about players that was added by club admin
    to tournament.
    """

    class Meta:
        verbose_name = "Tournament_Player"
        verbose_name_plural = "Tournament_Players"
        db_table = "tournament_players"

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )
