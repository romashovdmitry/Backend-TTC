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
    TournamentPlayers,
    Tournament
)

# import constants
from tournament.constants import TournamentStage

# import custom foos, classes
from telegram_bot.send_error import telegram_log_errors


async def divide_players_to_groups(
        group_qualifiers_number: int,
        tournament_pk: int,
        tournament_players: list[TournamentPlayers],
        group_number: int | None = None,
        group_players_number: int | None = None,
) -> bool:
    """
    FIXME: дописать аннотирование. не горит. 
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
    # FIXME: это 100% можно зарефакторить. 
    # часть кода писалась во время созвона и HotFix-ы. 
    try:
        tournament_players = await sync_to_async(list)(tournament_players)

        # Is user chose groups number.
        # Than we define numbber of group players
        if group_number:
            flag = False
            group_players_number = len(tournament_players) // group_number
            
            if group_players_number == 0:
                
                return False

        # If user chose group player number.
        # Than we define number of groups
        elif group_players_number:
            flag = True
            group_number = len(tournament_players) // group_players_number

            if group_number == 0:

                return False

        free_players = len(tournament_players) - (group_number * group_players_number)

        if free_players > 0 and not free_players == 1 and flag:
            group_number += 1

        if free_players <= 2:
    
            if flag and not free_players == 1:
                
                return False

        if group_players_number <= 2:
            return False

        if free_players > 1 and \
           group_players_number - free_players > 1:

            return False

        await Tournament.objects.filter(
            pk=tournament_pk
        ).aupdate(
            group_players_number=group_players_number
        )

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
