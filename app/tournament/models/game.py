# import basemodel and django.db.models
from main.base_model import models

# import models
from user.models import Player
from tournament.models import Tournament, TournamentPlayers

# import constants
from tournament.constants import GameStatus


class Game(models.Model):
    """
    Class for saving tournament's Games.
    """
    class Meta:
        db_table = "games"
        verbose_name = "Game"
        verbose_name_plural = "Games"

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        null=True,
        related_name="games_of_tournament",
        verbose_name="Tournament",
        help_text="Tournament"
    )
    first_player = models.ForeignKey(
        TournamentPlayers,
        on_delete=models.CASCADE,
        related_name="games_first_player",
        verbose_name="One of two players of game",
        help_text="One of two players of game"
    )
    second_player = models.ForeignKey(
        TournamentPlayers,
        on_delete=models.CASCADE,
        # NOTE: is second player is None - it means, that
        # player is waiting for next game (do nothing). 
        # e.g. in 5 players group it's usual scenario.
        null=True,
        related_name="games_second_player",
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
    status = models.PositiveSmallIntegerField(
        choices=GameStatus,
        null=True,
        verbose_name="Game's status: created, started or finished",
        help_text="Game's status: created, started or finished"        
    )
    order = models.PositiveSmallIntegerField(
        null=True,
        verbose_name="Order of game inside group stage",
        help_text="Order of game inside group stage"
    )

    def __return_game_winner(self):
        """ return Player instance of winner in game"""
        return self.first_player if \
            self.first_player_score > self.second_player_score else \
            self.second_player
