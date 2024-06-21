# Django imports
from django.urls import path

# custom DRF classes imports
from tournament.views import (
    TournamentActions,
)

# urls without pk in URL PATH params
tournament_actions = TournamentActions.as_view({"post": "create_tournament"})


urlpatterns = [
    path('', tournament_actions, name="tournament_actions"),
]