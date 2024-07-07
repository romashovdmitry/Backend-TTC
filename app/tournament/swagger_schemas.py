# Swagger imports
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes

# import serailizers
from tournament.serializers import TournamentListSerializer


swagger_schema_tournament_create = extend_schema(
        tags=["Tournament"],
        summary="Create new Tournament",
        description="POST request to create new Tournament",
        operation_id="Create new Tournament",
        request={
            "application/json": {
                "example": {
                    "name": "Men Fusk Mens - it's real sport!",
                    "date_time": "2024-07-03T22:14:00+04:00",
                    "club": 1
                }
            }
        },
    )


swagger_schema_tournament_list = extend_schema(
        tags=["Tournament"],
        methods=["GET"],
        summary="Get configured Tournaments",
        description="GET request to get configured Tournaments",
        operation_id="Get configured Tournaments",
        responses={
            201: OpenApiResponse(response=TournamentListSerializer,
                                 description='Configured Tournaments in response'),
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


swagger_schema_admin_my_tournament_list = extend_schema(
        tags=["Tournament"],
        methods=["GET"],
        summary="Get by admin my tournamets",
        description="GET request to get admin's Tournaments",
        operation_id="Get admin's Tournaments"
)

swagger_schema_add_player_to_tournament = extend_schema(
        tags=["Tournament"],
        methods=["PUT"],
        summary="Add player to tournament",
        description="PUT request to add player to tournament",
        operation_id="Add player to tournament",
        request={
            "application/json": {
                "example": {
                    "tournament": 1,
                    "player": 1
                }
            }
        },
    )       
