# Django imports
from django.urls import path

# custom DRF classes imports
from club.views import ClubCreateUpdate


club_actions = ClubCreateUpdate.as_view({"post": "create_club", "patch": "update_club"})


urlpatterns = [
    path('', club_actions, name="club_actions"),
]