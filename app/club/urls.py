# Django imports
from django.urls import path

# custom DRF classes imports
from club.views import (
    ClubActions,
    ClubPhotosDestroyCreateView
)


# urls without pk in URL PATH params
club_create_update_get = ClubActions.as_view(
    {
        "post": "create_club",
        "get": "list_clubs"
    }
)

# urls with pk in URL PATH params
get__update_club = ClubActions.as_view(
    {
        "put": "update_club",
        "get": "get_club"
    }
)


urlpatterns = [
    path('', club_create_update_get, name="club_actions"),
    path('club/<int:id>/', get__update_club, name="get_club"),
    path('photo/<int:id>/', ClubPhotosDestroyCreateView.as_view(), name='club_photo_endpoint')
]