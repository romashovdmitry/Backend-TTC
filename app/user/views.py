# Python imports
import json
import asyncio

# DRF imports
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser

# import serializers
from user.serializers import (
    CreateUserSerializer,
    UpdatePlayerSerializer,
    LoginUserSerializer,
    GetPlayerInfoSerializer,
    UpdateCreatePlayerPhotoSerializer,
    GetPeriodicalPlayerRating
)

# import models
from user.models import (
    User,
    Player,
    PlayerRatingHistory
)

# import constants, config data
from main.settings import HTTP_HEADERS
from user.constants import GeoChoiсe

# import swagger schemas
from user.swagger_schemas import (
    swagger_schema_create_user,
    swagger_schema_login_user,
    swagger_schema_update_player,
    swagger_schema_get_player,
    swagger_schema_create_update_player_photo,
    swagger_schema_get_periodical_player_rating,
    swagger_schema_get_cities
)

# import custom foos, classes
from user.services import hashing, JWTActions
from telegram_bot.send_error import telegram_log_errors


class UserCreateUpdate(ViewSet):
    """ class for creating and updating users """
    http_method_names = ['post', 'update']
    lookup_field = 'id'
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        """ define serializer for class """
        if self.action == 'create_user':
            return CreateUserSerializer
        return LoginUserSerializer

    @swagger_schema_create_user
    @action(detail=False, methods=['post'], url_path="create_user")
    def create_user(self, request) -> Response:
        """
        1. Creating new user instance in Model.
        2. Create JWT-pare.
        3. Set JWT-pare on cookies.
        4. Return response with JWT.
        """
        try:
            serializer = self.get_serializer_class()
            serializer = serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                instance = serializer.save()
                # go to hash password
                instance.password = asyncio.run(hashing(
                    validated_data['password'],
                ))
                instance.save()
                return_response = HttpResponse(
                    status=HTTP_201_CREATED,
                    headers=HTTP_HEADERS,
                    content=json.dumps(
                        {
                            "user_id": instance.id
                        }
                    )
                )

                return asyncio.run(
                    JWTActions(
                        response=return_response,
                        instance=instance                
                    ).set_cookies_on_response()
                )

            else:

                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f'[UserCreateUpdate][create_user] {str(ex)}'
                )
            )
            return Response(
                str(ex),
                status=HTTP_400_BAD_REQUEST,
            )

    @swagger_schema_login_user
    @action(detail=False, methods=['post'], url_path="login_user")
    def login_user(self, request) -> Response:
        ''' login user '''
        try:
            serializer = self.get_serializer_class()
            serializer = serializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                user = User.objects.filter(email=serializer.validated_data["email"]).first()
                return_response = HttpResponse(
                    status=HTTP_200_OK,
                    headers=HTTP_HEADERS,
                    content=json.dumps(
                        {
                            "email": validated_data["email"]
                        }
                    )
                )
                return asyncio.run(
                    JWTActions(
                            response=return_response,
                            instance=user
                        ).set_cookies_on_response()
                )

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f'[UserCreateUpdate][login_user] {ex}'
                )
            )
            return Response(
                ex,
                status=HTTP_400_BAD_REQUEST,
            )


class PlayerGetUpdate(ViewSet, RetrieveAPIView):
    """ class for creating and updating users """
    http_method_names = ['post', 'put', 'get']
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, )
    queryset = Player.objects.all()

    serializer_map = {
        'update_player': UpdatePlayerSerializer,
        'get_player': GetPlayerInfoSerializer,
        "create_update_player_photo": UpdateCreatePlayerPhotoSerializer,
        "get_periodical_player_rating": GetPeriodicalPlayerRating
    }

    def get_queryset(self):
        """ get queryset """        
        if self.action == "get_periodical_player_rating":
        
            return PlayerRatingHistory.objects.filter(
                player__user=self.request.user
            ).all()

    def get_serializer_class(self):
        """ define serializer for class """

        return self.serializer_map[self.action]

    @swagger_schema_create_update_player_photo
    @action(
        detail=False,
        methods=['put'],
        url_path="create_update_player_photo",
        parser_classes=(MultiPartParser,)
    )
    def create_update_player_photo(self, request) -> Response:
        """ update player photo """
        try:
            instance = Player.objects.filter(user=request.user).first()

            if instance:
                serializer = self.get_serializer_class()
                serializer = serializer(instance=instance, data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    return Response(
                        status=HTTP_200_OK                
                    )

            else:

                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f'[UserCreateUpdate][create_player] {ex}'
                )
            )
            return Response(
                data=(
                    f'Not valid JSON. Error text: {ex}'
                ),
                status=HTTP_400_BAD_REQUEST
            )

    @swagger_schema_update_player
    @action(
        detail=True,
        methods=['put'],
        url_path="update_player",
        parser_classes=(
            MultiPartParser,
            JSONParser,
            FormParser
        )
    )
    def update_player(self, request) -> Response:
        """ updating player info """
        try:
            instance = Player.objects.filter(user=request.user).first()

            if instance:
                serializer = self.get_serializer_class()
                serializer = serializer(instance=instance, data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.update(
                        instance=instance,
                        validated_data=serializer.validated_data
                    )

                    return Response(
                        status=HTTP_200_OK                
                    )
            
                else:

                    return Response(
                        serializer.errors,
                        status=HTTP_400_BAD_REQUEST
                    )

            else:
                return Response(HTTP_400_BAD_REQUEST)

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[ClubActions][update_club] {str(ex)}"
                )
            )
        
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST
            )
    
    @swagger_schema_get_player
    @action(
        detail=True,
        methods=['get'],
        url_path="get_player",
        parser_classes=(MultiPartParser,)
    )
    def get_player(self, request) -> Response:
        """ return info about certain player """
        try:
            player = Player.objects.get(
                user=request.user
            )
            serialiser = self.get_serializer_class()
            serialiser = serialiser(player)

            return Response(serialiser.data)

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[ClubActions][get_player] {str(ex)}"
                )
            )
        
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST
            )

    @swagger_schema_get_periodical_player_rating
    @action(
        detail=False,
        methods=['get'],
        url_path="get_periodical_player_rating",
        parser_classes=(MultiPartParser,)
    )
    def get_periodical_player_rating(self, request) -> Response:
        """ return info about player's rating """

        try:
            queryset = self.get_queryset()

            if queryset:
                serialiser = self.get_serializer_class()
                serialised_queryset = serialiser(
                    queryset,
                    many=True
                )

                return Response(
                    status=HTTP_200_OK,
                    data=serialised_queryset.data
                )

            return Response(
                status=HTTP_200_OK,
                data=None
            )

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    "[ClubActions][get_periodical_player_rating] "
                    f"{str(ex)}"
                )
            )
        
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST
            )
        

class GetCities(APIView):
    """
    Simple view, that returns
    list of cities
    """
    @swagger_schema_get_cities
    def get(self, request):

        try:
            return Response(
                [{"id": item[0], "name": item[1]} for item in GeoChoiсe]
            )

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    "[GetCities] "
                    f"{str(ex)}"
                )
            )
        
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST
            )