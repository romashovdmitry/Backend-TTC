# Django imports
from django.urls import path

# custom DRF classes imports
from user.views import UserCreateUpdate, PlayerCreateUpdate

# JWT imports
from rest_framework_simplejwt.views import TokenRefreshView

user_actions = UserCreateUpdate.as_view({"post": "create_user"})
player_actions = PlayerCreateUpdate.as_view({"post": "create_player"})


urlpatterns = [
    path('', user_actions, name="user_actions"),
    path('player/', player_actions, name="create_player"),
    path('refresh_token/', TokenRefreshView.as_view(), name="refresh_token"),
]