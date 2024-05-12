# Python imports
import json
import asyncio

# DRF imports
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

# import serializers
from user.serializers import (
    CreateUserSerializer,
    CreateUpdatePlayerSerializer,
    LoginUserSerializer
)


# Swagger imports
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes



# import constants, config data
from user.models.user import User
from main.settings import HTTP_HEADERS

# import custom foos, classes
from user.services import hashing, JWTActions


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
                    "last_name": "pizdalov",
                    "birth_date": "2000-01-01"
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
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)

        if serializer.is_valid():
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
                        "email": validated_data["email"]
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
        print('com to log')
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            print(f'val dat - . {serializer.validated_data}')
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
            print(user)
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


class PlayerCreateUpdate(ViewSet):
    """ class for creating and updating users """
    http_method_names = ['post', 'update']
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """ define serializer for class """
        if self.action == 'create_player':
            return CreateUpdatePlayerSerializer

    @extend_schema(
        tags=["User"],
        summary="Create player instance for existing user",
        description="POST request to create player instance for existing user",
        auth=None,
        operation_id="Create player instance for existing user",
        parameters=[
            OpenApiParameter(
                name="sex",
                description='Sex of user. MALE or FEMALE',
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Player sex',
                        value='FEMALE'
                    ),
                ],
            ),
            OpenApiParameter(
                name='handedness',
                type=OpenApiTypes.STR,
                description=(
                        "User's handedness. "
                        "RIGHT_HAND, LEFT_HAND "
                        "or BOTH"
                ),
                examples=[
                    OpenApiExample(
                        'Which hand player gona play',
                        value='BOTH'
                    ),
                ],
            ),
            OpenApiParameter(
                name='rating',
                required=False,
                type=OpenApiTypes.INT,
                description=(
                        "Rating of user in our system. " 
                        "100 by default"
                ),
                examples=[
                    OpenApiExample(
                        'User Raing in our system',
                        value=200
                    ),
                ],
            ),
            OpenApiParameter(
                name='user info',
                required=["first_name", "last_name"],
                type=OpenApiTypes.OBJECT,
                description=(
                        "Rating of user in our system. " 
                        "100 by default"
                ),
                examples=[
                    OpenApiExample(
                        'User Oject with first name name and last name',
                        value={
                            "last_name": "Ivanov",
                            "first_name": "Kaktus"
                        }
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
                    "sex": "FEMALE",
                    "handedness": "BOTH",
                    "rating": 69,
                    "user": {
                        "last_name": "Doe",
                        "first_name": "John"
                    }
                }
            ),
        ],
        responses={
            200: None,
        }
    )
    @action(detail=False, methods=['post'], url_path="create_player")
    def create_player(self, request) -> Response:
        """ creating new player """
        try:
            serializer = self.get_serializer_class()
            print(request.data)
            serializer = serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                instance = serializer.save()
                instance.save()

                return Response(
                    status=HTTP_201_CREATED,
                    data={
                        "playest": validated_data
                    }
                )

            else:

                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        except Exception as ex:

            return Response(
                data=(
                    f'Not valid JSON. Error text: {ex}'
                ),
                status=HTTP_400_BAD_REQUEST
            )
