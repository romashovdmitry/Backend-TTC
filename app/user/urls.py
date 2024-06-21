# Django imports
from django.urls import path

# custom DRF classes imports
from user.views import (
    UserCreateUpdate,
    PlayerGetUpdate
)

# JWT imports
from rest_framework_simplejwt.views import TokenRefreshView

user_actions = UserCreateUpdate.as_view({"post": "create_user"})
login_user = UserCreateUpdate.as_view({"post": "login_user"})
player_actions = PlayerGetUpdate.as_view({"put": "update_player", "get": "get_player"})
player_create_photo = PlayerGetUpdate.as_view({"put": "create_update_player_photo"})

urlpatterns = [
    path('', user_actions, name="user_actions"),
    path('login_user/', login_user, name="login_user"),
    path('player/', player_actions, name="create_player"),
    path('player/photo/', player_create_photo, name="player_create_photo"),
    # JWT
    path('refresh_token/', TokenRefreshView.as_view(), name="refresh_token"),
]