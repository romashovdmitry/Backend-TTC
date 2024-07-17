# Python imports
import asyncio
from typing import Tuple

# async imports
from asgiref.sync import sync_to_async

# Django imports
# DRF imports
# Serializers imports
# Swagger Schemas imports

# import models
from tournament.models import (
    TournamentPlayers,
    Tournament,
    Game
)

# import constants
from tournament.constants import TournamentStage, GameStatus

# import custom foos, classes
from telegram_bot.send_error import telegram_log_errors


async def divide_players_to_groups(
        group_qualifiers_number: int,
        tournament_pk: int,
        tournament_players: list[TournamentPlayers],
        group_number: int | None = None,
        group_players_number: int | None = None,
) -> Tuple[bool, int | None]:
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
    Returns:
        bool: success or not
        int | None: group number if bool True or None if
            bool False. That's because of group number could
            be changed in foo process.
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

        return True, group_number

    except Exception as ex:
        await telegram_log_errors(
            f"[TournamtneActions][create_tournament] {str(ex)}"
        )

        return False, None


def create_tournament_games(
    tournament_pk: int,
    tournament_players: list[TournamentPlayers],
    group_number: int,
    **kwargs
) -> None:
    """
    Create games for tournament. 
    NOTE: there are other params but we don't use them.
    Parameters:
        group_number: amount of groups in tournament
        tournament_pk: tournament primary key
        tournament_players: players added to participate
            in tournament
    """
    for group_order in range(1, group_number + 1):
        group_players: list[TournamentPlayers] = list(
            TournamentPlayers.objects.filter(
                tournament_id=tournament_pk,
                tournament_group=group_order
            ).all()
        )
        group_players_copy = group_players.copy()

        games_stack: list[Game] = []

        while len(group_players_copy) > 2:

            for group_player in range(1, len(group_players_copy)):
                games_stack.append(
                    Game.objects.create(
                        first_player=group_players_copy[0],
                        second_player=group_players_copy[group_player],
                        status=GameStatus.CREATED,
                        tournament_id=tournament_pk
                    )
                )
            
            group_players_copy.pop(0)

        games_stack.append(
            Game.objects.create(
                    first_player=group_players_copy[0],
                    second_player=group_players_copy[1],
                    status=GameStatus.CREATED,
                    tournament_id=tournament_pk
                )
            )
        # сколько игр может происходит одновременно в
        # рамках одной группы
        one_time_tables = (len(group_players) // 2)

        if len(group_players) % 2 != 0:
            for group_player in group_players:
                games_stack.append(
                    Game.objects.create(
                        first_player=group_player,
                        second_player=None,
                        status=GameStatus.CREATED,
                        tournament_id=tournament_pk
                    )
                )
            # but one would be (player VS None) Game object
            one_time_tables = (len(group_players) // 2) + 1

        # сколько каждый игрок должен сыграть игр
        # len(group_players)
        for game_order in range(1, len(group_players)+1):
            player_stack = []
            i = 0
            game_stack_next_iter = 0
            while game_stack_next_iter != len(games_stack):
                game = games_stack[game_stack_next_iter]

                # NOTE: только второй игрок может быть None
                if not game.second_player:
                    game.order = game_order
                    game.save()
                    player_stack.append(game.first_player.pk)
                    games_stack.remove(game)
                    i += 1

                elif game.first_player.pk not in player_stack\
                        and game.second_player.pk not in player_stack:

                    player_stack.append(game.first_player.pk)
                    player_stack.append(game.second_player.pk)
                    game.order = game_order
                    game.save()
                    games_stack.remove(game)
                    i += 1

                else:
                    game_stack_next_iter += 1

                if i >= one_time_tables:
                    break


def create_tournament_grid(
        tournament_pk: int,
        **kwargs
):
    """
    Create tournament grid, that backend send to
        frontend to show to tournament's admin
    Parameters:
            tournament_pk: tournament primary key    
    """
    pass