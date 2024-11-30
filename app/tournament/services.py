# Python imports
import asyncio
from typing import Tuple

# async imports
from asgiref.sync import sync_to_async

# Django imports
from django.db.models import Q
# DRF imports
# Serializers imports
# Swagger Schemas imports

# import models
from tournament.models import (
    TournamentPlayers,
    Tournament,
    Game,
    KnockoutGame
)

# import constants
from tournament.constants import (
    TournamentStage,
    GameStatus,
    GROUP_ALPHABBET
)

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
            flag = False  # False -> we have amount of groups
            group_players_number = len(tournament_players) // group_number
            
            if group_players_number == 0:
                
                return False, None

        # If user chose group player number.
        # Than we define number of groups
        elif group_players_number:
            flag = True  # True -> we have amount of players in one group
            group_number = len(tournament_players) // group_players_number

            if group_number == 0:

                return False, None

        free_players = len(tournament_players) - (group_number * group_players_number)

        if flag and free_players > group_number:

            return False, None

        if group_players_number <= 2:

            return False, None

        await Tournament.objects.filter(
            pk=tournament_pk
        ).aupdate(
            group_players_number=group_players_number,
            group_number=group_number
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
) -> tuple[bool, dict]:
    """
    Create games for tournament. 
    NOTE: there are other params but we don't use them.
    Parameters:
        group_number: amount of groups in tournament
        tournament_pk: tournament primary key
        tournament_players: players added to participate
            in tournament
    Returns:
        bool: success or not
        dict: dict where key is number of group and
            value is list of games inside group
    """

    previous_games = Game.objects.filter(tournament=tournament_pk).all()

    if previous_games:
        [previous_game.delete() for previous_game in previous_games]

    try:
        return_dict = {}

        for group_order in range(1, group_number + 1):
            return_dict[group_order] = []
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
                            tournament_id=tournament_pk,
                            group_number=group_players_copy[0].tournament_group
                        )
                    )
                
                group_players_copy.pop(0)

            games_stack.append(
                Game.objects.create(
                        first_player=group_players_copy[0],
                        second_player=group_players_copy[1],
                        status=GameStatus.CREATED,
                        tournament_id=tournament_pk,
                        group_number=group_players_copy[0].tournament_group
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
                            tournament_id=tournament_pk,
                            group_number=group_player.tournament_group
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
                    if not game.second_player and \
                    game.first_player.pk not in player_stack:
                        game.order = game_order
                        game.save()
                        return_dict[group_order].append(game)
                        player_stack.append(game.first_player.pk)
                        games_stack.remove(game)
                        i += 1

                    elif game.first_player.pk not in player_stack\
                            and game.second_player.pk not in player_stack:

                        player_stack.append(game.first_player.pk)
                        player_stack.append(game.second_player.pk)
                        game.order = game_order
                        game.save()
                        return_dict[group_order].append(game)
                        games_stack.remove(game)
                        i += 1

                    else:
                        game_stack_next_iter += 1

                    if i >= one_time_tables:
                        break

        return True, return_dict


    except Exception as ex:
        asyncio.run(
            telegram_log_errors(
                f"[create_tournament_games] {str(ex)}"
            )
        )

        return False, None


def create_tournament_grid(
        games_dict: dict,
        **kwargs
):
    """
    Create tournament grid, that backend send to
        frontend to show to tournament's admin
    Parameters:
            games_dict: dict where key is number of group and
                value is list of games inside group
    """
    return_dict = {"groups": []}
    group_number = kwargs["group_number"]

    for group in range(1, group_number+1):
        group_dict = {}
        group_players: TournamentPlayers = TournamentPlayers.objects.filter(
            tournament_group=group
        ).all()
        group_dict["group_id"] = group
        group_dict["group_alpha"] = GROUP_ALPHABBET[group]

        grid_id = 0 
        group_players_list = []

        for group_player in group_players:
            grid_id += 1
            group_players_list.append(
                {
                    "pk": group_player.player.user.pk,
                    "grid_id": grid_id,
                    "name": group_player.player.user.full_name
                }
            )

        group_dict["players"] = group_players_list
        group_dict['group_games'] = []

        for game in games_dict[group]:
            group_dict['group_games'].append(
                {
                    "game_pk": game.pk,
                    "game_order": game.order,
                    "first_player_tournament_pk": game.first_player.pk,
                    "second_player_tournament_pk": game.second_player.pk if game.second_player else None,
                    "first_player_score": game.first_player_score,
                    "second_player_score": game.second_player_score
                }
            )

        return_dict["groups"].append(group_dict)
    
    return return_dict


def get_tournament_grid(
    tournament_obj: Tournament
):
    """
    documentation
    """
    return_dict = {"groups": []}
    group_number = tournament_obj.group_number

    for group in range(1, group_number+1):
        group_dict = {}
        group_players: TournamentPlayers = TournamentPlayers.objects.filter(
            tournament_group=group
        ).all()
        group_dict["group_id"] = group
        group_dict["group_alpha"] = GROUP_ALPHABBET[group]

        grid_id = 0 
        group_players_list = []
    
        for group_player in group_players:
            grid_id += 1
            group_players_list.append(
                {
                    "pk": group_player.player.user.pk,
                    "grid_id": grid_id,
                    "name": group_player.player.user.full_name
                }
            )

        group_dict["players"] = group_players_list
        group_dict['group_games'] = []

        games = Game.objects.order_by('group_number')
        grouped_games = {}

        for game in games:
            group_number = game.group_number

            if group_number not in grouped_games:
                grouped_games[group_number] = []
            grouped_games[group_number].append(game)

        for game in grouped_games[group]:
            group_dict['group_games'].append(
                {
                    "game_pk": game.pk,
                    "game_order": game.order,
                    "first_player_tournament_pk": game.first_player.pk,
                    "second_player_tournament_pk": game.second_player.pk if game.second_player else None,
                    "first_player_score": game.first_player_score,
                    "second_player_score": game.second_player_score
                }
            )
        return_dict["groups"].append(group_dict)

    return return_dict


def sync_get_all_games_finished_or_not(tournament__):

    ttt: list[Tournament] = tournament__.games_of_tournament.all()

    for t in ttt:

        if t.status == GameStatus.STARTED or t.status == GameStatus.CREATED:

            return False

    return True


async def is_tournament_group_stage_finished(
        game_pk: Game.pk
):
    """
    проверяем закончился ли турнир
    """
    game: Game = await Game.objects.aget(pk=game_pk)
    # https://stackoverflow.com/a/74866708
    x = lambda: game.tournament
    af = sync_to_async(x)
    x = await af()
    return await sync_to_async(
        sync_get_all_games_finished_or_not
    )(x)


def get_players_with_max_points(
        group_qualifiers_number,
        tournament_results
):
    """
    Функция находит указанное количество лучших игроков с максимальным
    количеством очков.
    Если игроков больше, чем group_qualifiers_number, возвращает None.

    Args:
        group_qualifiers_number (int): Количество игроков, которое нужно
            отобрать.
        tournament_results (dict): Словарь с результатами турнира,
            где ключи - игроки, значения - очки.

    Returns:
        list: Список объектов игроков с максимальным количеством очков.
    """
    group_player_places_return = []

    if group_qualifiers_number > 2:
        
        return None

    place = 1
    while tournament_results:
        max_points = max(tournament_results.values())
        best_players = [
            player
            for player, points
            in tournament_results.items()
            if points == max_points
        ]

        if len(best_players) == 1:
            group_player_places_return.append(
                {
                    "place": place,
                    "player": best_players[0]
                }
            )
            del tournament_results[best_players[0]]
            place += 1

        elif len(best_players) == 2:

            game_of_best_group_player = Game.objects.filter(
                Q(first_player=best_players[0], second_player=best_players[1]) |
                Q(first_player=best_players[1], second_player=best_players[0])
            ).first()
            group_player_places_return.append(
                {
                    "place": place,
                    "player": game_of_best_group_player.return_game_winner
                }
            )
            del tournament_results[
                game_of_best_group_player.return_game_winner
            ]
            place += 1

        else:

            return None

    # FIXME: дерьмо, править надо, дважды сораздется пара place -> value
    return [
        {
            "place": dict_item["place"],
            "player_pk": dict_item["player"].pk
        }
        for dict_item
        in group_player_places_return
    ]


def create_groups_game_rating(
        tournament: Tournament
):
    """
    FIXME: documentation
    create knockout you know (:
    """
    knockout_players = []
    game_results_dict = {}
    all_tournament_players: list[TournamentPlayers] = tournament.tournament_players.all()
    all_tournament_games: list[Game] = tournament.games_of_tournament.all()
    [   
        game_results_dict.update(
            {
                t_group_number: {}
            }
        )
        for t_group_number
        in range(
            1, tournament.group_number + 1
        )
    ]

    for tournament_player in all_tournament_players:
        game_results_dict[tournament_player.tournament_group].update({tournament_player: None})

    for tournament_group in game_results_dict:
        
        for tournament_player in game_results_dict[tournament_group]:
            player_games = (
                tournament_player.games_first_player.all()
            ).union(
                tournament_player.games_second_player.all()
            )

            points = 0

            for game in player_games:

                if game.return_game_winner == tournament_player:
                    points += 1
            game_results_dict[tournament_group][tournament_player] = points

    # {1: {TournamentPlayers object: 3, ...}, 2: {}}
    # первыи ключ - это номер группы. значением словарь, где идет игрок и его кол-во побед.
    for games_group in game_results_dict:
        group_players_win_rating = get_players_with_max_points(
            group_qualifiers_number=tournament.group_qualifiers_number,
            tournament_results=game_results_dict[
                games_group
            ]
        )

        if group_players_win_rating:
            knockout_players.append(
                {
                    "group_number": games_group,
                    "games_rating": group_players_win_rating
                }
            )
    
        else:

            knockout_players.append(
                {
                    "group_number": games_group,
                    "games_rating": None
                }
            )
    # если есть словарь, значит для однои группы не проставились пары
    if not any(isinstance(item, dict) for item in knockout_players):
        pass
#        knockout_games = create_knockout_games_objects(
#            knockout_players,
#            len(game_results_dict),
#            tournament.group_qualifiers_number
#        )
#        return knockout_games

    return knockout_players


def create_knockout_games_objects(
        knockout_players: list[TournamentPlayers],
        group_qualifiers_number
):
    x = []
    y = 0

    while knockout_players:

        if (
            y + group_qualifiers_number
        ) < len(knockout_players):
            first_player: TournamentPlayers = knockout_players.pop(y)
            second_player: TournamentPlayers = knockout_players.pop(
                y + group_qualifiers_number - 1
            )
            # NOTE: это лучше перепроверить. из-за работы метода pop.
            
            x.append(
                {
                    "first_player": {
                        'pk': first_player.pk,
                        "full_name": first_player.player.user.return_full_name()
                    },
                    "second_player": {
                        "pk": second_player.pk,
                        "full_name": second_player.player.user.return_full_name()
                    }
                }
            )
            y += group_qualifiers_number

        elif len(knockout_players) == 2:
            first_player = knockout_players.pop(0)
            second_player = knockout_players.pop(0)
            x.append(
                {
                    "first_player": {
                        "pk": first_player.pk,
                        "full_name": first_player.player.user.return_full_name()
                    },
                    "second_player": {
                        "pk": second_player.pk,
                        "full_name": second_player.player.user.return_full_name()
                    }
                }
            )

        elif len(knockout_players) == 1:
            first_player = knockout_players.pop(0)
            x.append(
                {
                    "first_player": {
                        "pk": first_player.pk,
                        "full_name": first_player.player.user.return_full_name()
                    },
                    "second_player": None
                }
            )
        else:
            y = 0

    return x


def create_knockout(
        tournament: Tournament,
        data: dict
):

    try:
        tournament_player = []
        for element in data:
            for element__ in element["games_rating"]:
        
                tournament_player.append(
                    TournamentPlayers.objects.get(
                        pk=element__.get("player_pk")
                    )
                )
        

        knockout_games = create_knockout_games_objects(
            knockout_players=tournament_player,
            group_qualifiers_number=tournament.group_qualifiers_number
        )
        # pair - это TournamentPlayers объект
        for pair in knockout_games:
            knockout_game, created = KnockoutGame.objects.update_or_create(
                defaults={
                    "first_player": TournamentPlayers.objects.get(pk=pair["first_player"]["pk"]),
                    "second_player": TournamentPlayers.objects.get(pk=pair["second_player"]["pk"]),
                    "order": 1
                },
                first_player=TournamentPlayers.objects.get(pk=pair["first_player"]["pk"]),
                second_player=TournamentPlayers.objects.get(pk=pair["second_player"]["pk"])
            )
            pair['pk'] = knockout_game.pk

        return True, knockout_games

    except Exception as ex:
        asyncio.run(
            telegram_log_errors(
                f"[create_knockout] {str(ex)}"
            )
        )

        return False, []
