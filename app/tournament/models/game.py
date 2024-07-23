# import basemodel and django.db.models
from main.base_model import models

# import models
from user.models import Player
from tournament.models import Tournament


class Game(models.Model):
    """
    Class for saving tournament's Games.
    """
    class Meta:
        db_table = "games"
        verbose_name = "Game"
        verbose_name_plural = "Games"

    first_player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        verbose_name="One of two players of game",
        help_text="One of two players of game"
    )
    second_player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        verbose_name="One of two players of game",
        help_text="One of two players of game"
    )
    first_player_score = models.PositiveSmallIntegerField(
        null=True,
        default=0,
        verbose_name="How much sets first player wins",
        help_text="How much sets first player wins"
    )
    second_player_score = models.PositiveSmallIntegerField(
        null=True,
        default=0,
        verbose_name="How much sets second player wins",
        help_text="How much sets second player wins"
    )

    def __return_game_winner(self):
        """ return Player instance of winner in game"""
        return self.first_player if \
            self.first_player_score > self.second_player_score else \
            self.second_player
