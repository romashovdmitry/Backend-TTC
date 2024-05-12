# Django imports
from django.urls import path

# custom DRF classes imports
from club.views import ClubActions


club_create_update_get = ClubActions.as_view(
    {
        "post": "create_club",
        "get": "list_clubs"
    }
)

get__update_club = ClubActions.as_view(
    {
        "put": "update_club",
        "get": "get_club"
    }
)

urlpatterns = [
    path('', club_create_update_get, name="club_actions"),
    path('club/<int:id>/', get__update_club, name="get_club"),

]