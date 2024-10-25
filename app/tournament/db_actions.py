"""
FIXME: документирование.
пока тут оставляем отдельные операции с БД.
быстро делаем.
"""
# Python imports
import logging

logger = logging.getLogger(__name__)


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
        return True

    except Exception as ex:
        print(str(ex))
#        logger.error(
#            "tournament.db_actions.add_player | "
#            f"Exception text: {str(ex)}"
#        )
        return False
