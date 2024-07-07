# Django imports
from django.urls import path

# custom DRF classes imports
from tournament.views import (
    TournamentActions,
)

# urls without pk in URL PATH params
tournament_create___list_all_tournaments = TournamentActions.as_view(
    {
        "post": "create_tournament",
        "get": "list_tournament"
    }
)

tournament_admin_actions = TournamentActions.as_view(
    {
        "get": "list_my_tournaments",
        "put": "add_player_to_tournament"
    }
)


# admin_my - requests that admin is doing to change something
# in his clubs, tournaments, etc
urlpatterns = [
    path('', tournament_create___list_all_tournaments, name="tournament_actions"),
    path('admin_my/<int:club_pk>', tournament_admin_actions, name="tournament_admin_actions"),
    path('admin_my/add_player/', tournament_admin_actions, name="tournament_admin_actions")    
]