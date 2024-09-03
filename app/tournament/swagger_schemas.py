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


swagger_schema_add_player_to_tournament = extend_schema(
        tags=["Tournament"],
        # NOTE: PUT, not POST
        # because we updatin existing tournament
        methods=["PUT"],
        summary="Create tournament's groups, divide player to groups",
        description="PUT request to divide players to groups",
        operation_id="Divide players to groups",
        request={
            "application/json": {
                "example": {
                    "group_number": 3,
                    "group_players_number": 3,
                    "group_qualifiers_number": 1
                }
            }
        },
    )       


swagger_schema_game_start = extend_schema(
        tags=["Tournament"],
        # NOTE: PUT, not POST
        # because we updatin existing tournament
        methods=["PUT"],
        summary="To mark game as started",
        description="PUT request to mark game as started",
        operation_id="To mark game as started",
    )       


swagger_schema_game_result = extend_schema(
        tags=["Tournament"],
        # NOTE: PUT, not POST
        # because we updatin existing tournament
        methods=["PUT"],
        summary="To save game's result",
        description="PUT request to save game's result",
        operation_id="To save game's result",
        request={
            "application/json": {
                "example": {
                    "first_player_score": 2,
                    "second_player_score": 0
                }
            }
   
        }
    )       
