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
from user.serializers import CreateUserSerializer, CreateUpdatePlayerSerializer

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# import constants, config data
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

    @swagger_auto_schema(
        tags=["Create user"],
        operation_id="Create new user email and password",
        operation_description="POST request to create new user email, password",
        method="POST",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Email of user"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=(
                        "User's password. "
                        "Must contains digit, uppercase letter, "
                        "lowercase letter, 7 characters long and "
                        "not longer 20 characters. "
                    )
                )
            },
            required=["email", "password"],
            example={
                "email": "developerdmitry@gmail.com",
                "password": "123HJQnwebz78!!!"
            },
        ),

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


class PlayerCreateUpdate(ViewSet):
    """ class for creating and updating users """
    http_method_names = ['post', 'update']
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """ define serializer for class """
        if self.action == 'create_player':
            return CreateUpdatePlayerSerializer

    @swagger_auto_schema(
        tags=["Create player"],
        operation_id="Create new player name, additional info about player",
        operation_description=(
            "POST request to create new player name, "
            "additional info about player"
        ),
        method="POST",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "sex": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Sex of user. MALE or FEMALE"
                ),
                "handedness": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=(
                        "User's handedness. "
                        "RIGHT_HAND, LEFT_HAND"
                        "or BOTH"
                    )
                ),
                "rating": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description=(
                        "Rating of user. " 
                        "100 by default"
                    )
                ),
                "user": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    required=["last_name", "first_name"],  # Optional: Specify required properties
                    properties={
                        "last_name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="User's last name"
                        ),
                        "first_name": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="User's first name"
                        )
                    }
                )
            },
            required=["sex", "user"],
            example={
                "sex": "FEMALE",
                "handedness": "BOTH",
                "rating": 69,
                "user": {
                    "last_name": "Doe",
                    "first_name": "John"
                }
            },
        ),
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
