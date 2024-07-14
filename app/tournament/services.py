# Python imports
import asyncio

# async imports
from asgiref.sync import sync_to_async

# Django imports
# DRF imports
# Serializers imports
# Swagger Schemas imports

# import models
from tournament.models import (
    TournamentPlayers
)

# import constants
from tournament.constants import TournamentStage

# import custom foos, classes
from telegram_bot.send_error import telegram_log_errors


async def divide_players_to_groups(
        group_number: int,
        group_players_number: int,
        group_qualifiers_number: int,
        tournament_pk: int,
        tournament_players: list[TournamentPlayers],
) -> bool:
    """
    Foo divide plyers to groups after serialization
        of Put request for dividing.
    
        Rule for diving: max difference beetwen groups is
            one player. So, 3-3-4 it's ok.
            But 3-3-2 already not.

    Parameters:
        group_number: amount of groups in tournament
        group_players_number: amount of players in one
            group
        group_qualifiers_number: how much players could be
            get out to next stage of tournament
        tournament_pk: tournament primary key
        tournament_players: players added to participate
            in tournament
    """
    try:
        return_list_dicts = []
        tournament_players = await sync_to_async(list)(tournament_players)

        if len(tournament_players) % group_players_number > 1 and \
           group_players_number - (len(tournament_players) % group_players_number) > 1:

            return False
    
        else:
            # NOTE: номер группы в колличестве групп
            player_group = 1

            for player in tournament_players:

                player.tournament_group = player_group
                player.stage = TournamentStage.START
                await player.asave()

                if player_group + 1 > group_number:
                    player_group = 0

                player_group += 1

            return True

    except Exception as ex:
        await telegram_log_errors(
            f"[TournamtneActions][create_tournament] {str(ex)}"
        )

        return False
