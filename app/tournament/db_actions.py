"""
FIXME: документирование.
пока тут оставляем отдельные операции с БД.
быстро делаем.
"""
# Python imports
import logging
import asyncio

logger = logging.getLogger(__name__)

from tournament.services import update_player_rating


async def add_game_result(
    game_pk,
    first_player_score,
    second_player_score
):
    # import models
    from .models import Game
    # import constants
    from .constants import GameStatus

    try:
        await Game.objects.filter(pk=game_pk).aupdate(
            first_player_score=first_player_score,
            second_player_score=second_player_score,
            status=GameStatus.FINISHED
        )
        # FIXME: 2 запроса наалогичных к БД подряд.
        # не надо так. 
        game_ = Game.objects.aget(pk=game_pk)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, update_player_rating, game_pk)

        return True

    except Exception as ex:
        print(str(ex))
#        logger.error(
#            "tournament.db_actions.add_player | "
#            f"Exception text: {str(ex)}"
#        )
        return False


async def add_knock_game_result(
    game_pk,
    first_player_score,
    second_player_score
):
    # import models
    from .models import KnockoutGame
    # import constants
    from .constants import GameStatus

    try:

        await KnockoutGame.objects.filter(pk=game_pk).aupdate(
            first_player_score=first_player_score,
            second_player_score=second_player_score,
            status=GameStatus.FINISHED
        )
 
        return True

    except Exception as ex:
        print(str(ex))
#        logger.error(
#            "tournament.db_actions.add_player | "
#            f"Exception text: {str(ex)}"
#        )
        return False

from asgiref.sync import sync_to_async
@sync_to_async
def create_knock_game_result(
    tournament_pk,
    first_player_pk,
    second_player_pk,
    vertical_order,
    horizontal_order
):
    # import models
    from .models import KnockoutGame
    from tournament.models import Tournament, TournamentPlayers
    # import constants
    from .constants import GameStatus
    try:
        KnockoutGame.objects.create(
            tournament=Tournament.objects.get(pk=tournament_pk),
            first_player=TournamentPlayers.objects.get(pk=first_player_pk),
            second_player=TournamentPlayers.objects.get(pk=second_player_pk),
            vertical_order=vertical_order,
            horizontal_order=horizontal_order,
        )
        print('come here 2')
        return True

    except Exception as ex:
        print(str(ex))
#        logger.error(
#            "tournament.db_actions.add_player | "
#            f"Exception text: {str(ex)}"
#        )
        return False
