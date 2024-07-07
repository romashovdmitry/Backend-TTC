# Swagger imports
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes

# import serializers
from club.serializers import ClubGetSerializer
# import Swagger serializers
from club.swagger_serializer import SwaggerCreateUpdateClubPhotoSerializer


# import constants
from club.constants import OPENING_HOURS_SWAGGER_EXAMPLE


swagger_schema_club_get = extend_schema(
        tags=["Club"],
        methods=["GET"],
        summary="Get existing Club",
        description="GET request to get existing club by ID",
        operation_id="Get existing club by ID",
        responses={
            201: OpenApiResponse(response=ClubGetSerializer,
                                 description='Existing Club Object in response'),
            401: OpenApiResponse(
                response={
                    "detail": "No auth credentials"
                },
                description='No auth credentials.',
                examples=[
                    OpenApiExample(
                        "No auth credentials",
                        value={
                            "detail": "Authentication credentials were not provided."
                        }
                    )
                ]
            ),
        },
    )



swagger_schema_create_club = extend_schema(
        tags=["Club"],
        summary="Create new club",
        description='POST request to create new club',
        operation_id="Create new club",
        # NOTE:
        # OPENAPIexample gave wrong Swagger
        # interface. fix it by requests.
        request={
            "application/json": {
                "example": {
                    "name": "PussyGayClub",
                    "state": "Russia",
                    "city": "Saint-AbuDabi",
                    "address": "Chkalova 37",
                    "phone_number": "+79992370953",
                    "birth_date": "1994-05-26",
                    "about": "We love Penis! We hate Tennis!",
                    "social_link": "https://instagram.com/table_pennis",
                    "link": "https://welovechildrens.com/",
                    "opening_hours": OPENING_HOURS_SWAGGER_EXAMPLE,
                }
            }
        },
        # NOTE: можно добавить больше в responses, если будет время
        responses={
            201: None,
        }
    )



swagger_schema_update_club = extend_schema(
        tags=["Club"],
        summary="Update existing Club",
        description="PUT request to update existing club",
        # provide Authentication class that deviates from the views default
        operation_id="Update existing club",
        request={
            "application/json": {
                "example": {
                    "name": "PussyGayClub",
                    "state": "Russia",
                    "city": "Saint-AbuDabi",
                    "address": "Chkalova 37",
                    "phone_number": "+79992370953",
                    "birth_date": "1994-05-26",
                    "about": "We love Penis! We hate Tennis!",
                    "social_link": "https://instagram.com/table_pennis",
                    "link": "https://welovechildrens.com/",
                    "opening_hours": OPENING_HOURS_SWAGGER_EXAMPLE,
                }
            }
        },
        # NOTE: можно добавить больше в responses, если будет время
        responses={
            201: None,
        }
    )


swagger_schema_list_clubs = extend_schema(
        tags=["Club"],
        methods=["GET"],
        summary="Get all existing Clubs",
        description="GET request to get all existing clubs",
        operation_id="Get all existing clubs"
    )


swagger_schema_club_photo_delete = extend_schema(
        tags=["Club Photo"],
        methods=["DELETE"],
        summary="Delete club's photo",
        description="DELETE request to delete club's photo",
        operation_id="Delete club's photo"
    )

swagger_schema_club_photo_create = extend_schema(
        tags=["Club Photo"],
        methods=["POST"],
        summary="Create club's photo",
        description="Create request to create club's photo",
        operation_id="Create club's photo"
    )