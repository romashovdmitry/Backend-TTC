# Python imports
import json
import asyncio

# DRF imports
from rest_framework.viewsets import ViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.parsers import MultiPartParser

# import serializers
from user.serializers import (
    CreateUserSerializer,
    CreatePlayerSerializer,
    UpdatePlayerSerializer,
    LoginUserSerializer,
    GetPlayerInfoSerializer
)
from user.swagger_serializer import SwaggerCreatePlayerSerializer, SwaggerUpdatePlayerSerializer

# Swagger imports
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, PolymorphicProxySerializer
from drf_spectacular.types import OpenApiTypes

# import models
from user.models.player import Player

# import constants, config data
from user.models.user import User
from main.settings import HTTP_HEADERS

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

    @extend_schema(
        tags=["User"],
        summary="Create new user",
        description='POST request to create new user',
        auth=None,
        operation_id="Create new user",
        parameters=[
            OpenApiParameter(
                name='email',
                description='Email of the user',
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        'Email: STRING',
                        value='club_admin@mail.com'
                    ),
                ],
            ),
            OpenApiParameter(
                name='password',
                type=OpenApiTypes.STR,
                description=(
                    "User password "
                    "must contains digit, uppercase letter, "
                    "lowercase letter, 7 characters long and "
                    "not longer 20 characters. "
                ),
                examples=[
                    OpenApiExample(
                        'Password: STRING',
                        value='123njkQ6**N1q'
                    ),
                ],
            ),
            OpenApiParameter(
                name='First Name',
                type=OpenApiTypes.STR,
                description=(
                    "First name "
                ),
                examples=[
                    OpenApiExample(
                        'First Name: STRING',
                        value='Ivan'
                    ),
                ],
            ),
            OpenApiParameter(
                name='Last Name',
                type=OpenApiTypes.STR,
                description=(
                    "Last Name: STRING"
                ),
                examples=[
                    OpenApiExample(
                        'Last Name',
                        value='Pizdalov'
                    ),
                ],
            ),
            OpenApiParameter(
                name='Birth Date',
                type=OpenApiTypes.TIME,
                description=(
                    "Birth Date: DATE"
                ),
                examples=[
                    OpenApiExample(
                        'Birth Date',
                        value='2000-01-01'
                    ),
                ],
            ),
        ],
        examples=[
            OpenApiExample(
                'Example: succes created user',
                description=(
                    "User is a base model for player, "
                    "club admin, touernament admin"
                ),
                value={
                    "email": "club_admin@mail.com",
                    "password": "123njkQ6**N1q",
                    "first_name": "Ivan",
                    "last_name": "Pizdalov",
                    "birth_date": "1994-05-26"
                }
            ),
        ],
        # NOTE: можно добавить больше в responses, если будет время
        responses={
            201: None,
        }
    )
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

    @extend_schema(
        tags=["User"],
        summary="Login existing user",
        description='POST request to Login existing user',
        auth=None,
        operation_id="Login existing user",
        parameters=[
            OpenApiParameter(
                name='email',
                description='Email of the user',
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        'email example',
                        value='club_admin@mail.com'
                    ),
                ],
            ),
            OpenApiParameter(
                name='password',
                type=OpenApiTypes.STR,
                description=(
                    "User password "
                    "must contains digit, uppercase letter, "
                    "lowercase letter, 7 characters long and "
                    "not longer 20 characters. "
                ),
                examples=[
                    OpenApiExample(
                        'Password example',
                        value='123njkQ6**N1q'
                    ),
                ],
            ),
        ],
        examples=[
            OpenApiExample(
                'Example: succes login user',
                description=(
                    "User is a base model for player, "
                    "club admin, touernament admin"
                ),
                value={
                    "email": "club_admin@mail.com",
                    "password": "123njkQ6**N1q"
                }
            ),
        ],
        responses={
            200: None,
        }
    )
    @action(detail=False, methods=['post'], url_path="login_user")
    def login_user(self, request) -> Response:
        ''' login user '''
        try:
            serializer = self.get_serializer_class()
            serializer = serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
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


class PlayerGetCreateUpdate(ViewSet, RetrieveAPIView):
    """ class for creating and updating users """
    http_method_names = ['post', 'put', 'get']
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, )
    queryset = Player.objects.all()

    def get_serializer_class(self):
        """ define serializer for class """
        if self.action == 'create_player':

            return CreatePlayerSerializer

        elif self.action == "update_player":

            return UpdatePlayerSerializer

        return GetPlayerInfoSerializer

    @extend_schema(
        tags=["Player"],
        summary="Create player instance for existing user",
        description="POST request to create player instance for existing user",
        operation_id="Create player instance for existing user",
        request=SwaggerCreatePlayerSerializer,
        responses={
            200: None,
        },
    )
    @action(
        detail=False,
        methods=['put'],
        url_path="create_player",
        parser_classes=(MultiPartParser,)
    )
    def create_player(self, request) -> Response:
        """ creating new player """
        try:
            serializer = self.get_serializer_class()
            request.data["user"] = request.user
            serializer = serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                instance = serializer.create(
                    validated_data=validated_data,
                    user=request.user
                )

                return Response(
                    status=HTTP_201_CREATED
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

    @extend_schema(
        tags=["Player"],
        methods=["PUT"],
        summary="Update existing player info",
        description="PUT request to update player info",
        operation_id="Update player info",
        request=SwaggerUpdatePlayerSerializer,
        responses={
            200: None,
        },
    )
    @action(
        detail=True,
        methods=['put'],
        url_path="update_player",
        parser_classes=(MultiPartParser,)
    )
    def update_player(self, request) -> Response:
        """ updating player info """
        try:
            instance = Player.objects.filter(user=request.user).first()

            if instance:
                serializer = self.get_serializer_class()
                request.data["user"] = request.user
                serializer = serializer(instance=instance, data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    return Response(
                        status=HTTP_200_OK                
                    )
            
                else:

                    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

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
        
    @extend_schema(
        tags=["Player"],
        methods=["GET"],
        summary="Get info about Player",
        description="GET request to getplayer info",
        operation_id="Get player info",
        request=None,
        responses={
            200: None,
        },
    )
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