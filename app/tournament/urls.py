# Django imports
from django.urls import path

# custom DRF classes imports
from tournament.views import (
    TournamentActions,
    GameActions
)

# urls without pk in URL PATH params
tournament_create___list_all_tournaments = TournamentActions.as_view(
    {
        "post": "create_tournament",
        "get": "list_tournament"
    }
)

tournament_get_info_about_tournament_by_pk = TournamentActions.as_view(
    {
        "get": "get_info_about_tournament_by_pk"
    }
)

tournament_admin_actions = TournamentActions.as_view(
    {
        "get": "list_my_tournaments"
    }
)

# FIXME: полный отстой. надо hotfix, не до этого сейчас.
add_player_to_tournament = TournamentActions.as_view(
    {
        "put": "add_player_to_tournament"
    }
) 

tournament_groups_admin_actions = TournamentActions.as_view(
    {
        # NOTE: PUT, not POST
        # because we updatin existing tournament
        "put": "create_groups"
    }
)

game_actions = GameActions.as_view(
    {
        "put": "game_start"
    }
)

# admin_my - requests that admin is doing to change something
# in his clubs, tournaments, etc
urlpatterns = [
    path(
        '',
        tournament_create___list_all_tournaments,
        name="tournament_actions"
    ),
    path(
        'admin_my/<int:club_pk>',
        tournament_admin_actions,
        name="list_club_tournaments"
    ),
    path(
        'get_info_about/<int:tournament_pk>',
        tournament_get_info_about_tournament_by_pk,
        name="get_info_about_tournament_by_pk"
    ),
    path(
        'admin_my/add_player/',
        add_player_to_tournament,
        name="admin_add_player"
    ),
    path(
        'admin_my/create_groups/<int:tournament_pk>',
        tournament_groups_admin_actions,
        name="tournament_groups_admin_actions"
    ),
    path(
        'game/game_start/<int:game_pk>',
        game_actions,
        name="game_actions"
    )
]