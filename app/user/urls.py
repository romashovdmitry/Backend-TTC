# Django imports
from django.urls import path

# custom DRF classes imports
from user.views import UserCreateUpdate, PlayerGetCreateUpdate

# JWT imports
from rest_framework_simplejwt.views import TokenRefreshView

user_actions = UserCreateUpdate.as_view({"post": "create_user"})
login_user = UserCreateUpdate.as_view({"post": "login_user"})
player_create = PlayerGetCreateUpdate.as_view({"post": "create_player", "get": "get_player"})
player_update = PlayerGetCreateUpdate.as_view({"put": "update_player"} )

urlpatterns = [
    path('', user_actions, name="user_actions"),
    path('login_user/', login_user, name="login_user"),
    path('player/', player_create, name="create_player"),
    path('player/', player_update, name="update_player"),
    # JWT
    path('refresh_token/', TokenRefreshView.as_view(), name="refresh_token"),
]