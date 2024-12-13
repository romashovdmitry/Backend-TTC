# Swagger imports
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

# import swagger serializer
from user.swagger_serializer import (
    SwaggerUpdatePlayerSerializer,
    SwaggerCreateUpdatePlayerPhotoSerializer
)


swagger_schema_create_user = extend_schema(
        tags=["User"],
        summary="Create new user",
        description='POST request to create new user',
        auth=None,
        operation_id="Create new user",
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
                    "second_name": "Pizdalov",
                    "birth_date": "1994-05-26",
                    "sex": 1
                }
            ),
        ],
        # NOTE: можно добавить больше в responses, если будет время
        responses={
            201: None,
        }
    )


swagger_schema_login_user = extend_schema(
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


swagger_schema_update_player = extend_schema(
        tags=["Player"],
        methods=["PUT"],
        summary="Update existing player info",
        description="PUT request to update player info",
        operation_id="Update player info",
)

swagger_schema_get_player = extend_schema(
        tags=["Player"],
        methods=["GET"],
        summary="Get info about Player",
        description="GET request to get player info",
        operation_id="Get player info",
        request=None,
        responses={
            200: None,
        },
    )


swagger_schema_create_update_player_photo = extend_schema(
        tags=["Player"],
        summary="Update player photo for existing user",
        description="PUT request Update player photo for existing user",
        operation_id="Update player photo for existing user",
        request=SwaggerCreateUpdatePlayerPhotoSerializer,
        responses={
            200: None,
        },
    )


swagger_schema_get_periodical_player_rating = extend_schema(
    tags=["Player"],
    summary="Get player's rating for certain period. ",
    description="GET request to retrieve rating of player for certain period",
    operation_id="Get rating of user for certain period",
    request=None,
    responses={
        200: None,
    },
)


swagger_schema_get_cities = extend_schema(
    tags=["Cities"],
    summary="Get list of cities ",
    description="GET request to retrieve list of cities",
    operation_id="Get list of cities",
    request=None,
    responses={
        200: None,
    },
)

swagger_schema_get_all_players_rating = extend_schema(
    tags=["Player"],
    summary="Get ordered list of all player's rating",
    description="GET request to retrieve list of ordered player's rating",
    operation_id="Get ordered list of all player's rating",
    request=None,
    responses={
        200: None,
    },
)