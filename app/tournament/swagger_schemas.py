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

swagger_schema_get_info_about_tournament_by_pk = extend_schema(
        tags=["Tournament"],
        methods=["GET"],
        summary="Get info about tournament by PK",
        description="GET request to get info about tournament",
        operation_id="Get Tournament's info by PK"
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


swagger_schema_create_groups = extend_schema(
        tags=["Tournament"],
        # NOTE: PUT, not POST
        # because we updatin existing tournament
        methods=["PUT"],
        summary="Create tournament groups",
        description="Create tournament groups",
        operation_id="Create tournament groups",
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

swagger_schema_create_groups_game_rating = extend_schema(
        tags=["Tournament"],
        methods=["POST"],
        summary="Create groups game rating ",
        description="Create groups game rating",
        operation_id="Create groups game rating"
    )       

swagger_schema_get_groups = extend_schema(
        tags=["Tournament"],
        methods=["GET"],
        summary="Get tournament groups",
        description="Get tournament groups",
        operation_id="Get tournament groups",
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


# не доработана
swagger_schema_tournament_create_knockout = extend_schema(
        tags=["Tournament"],
        # NOTE: PUT, not POST
        # because we updatin existing tournament
        methods=["POST"],
        summary="To create knockout",
        description="POST request to create knockout",
        operation_id="To create knockout",
        request={
            "application/json": {
                "example": 
                    [
                        {
                            "group_number": 1,
                            "games_rating": [
                            {
                                "place": 1,
                                "player_pk": 11
                            },
                            {
                                "place": 2,
                                "player_pk": 9
                            },
                            {
                                "place": 3,
                                "player_pk": 1
                            },
                            {
                                "place": 4,
                                "player_pk": 5
                            }
                            ]
                        },
                        {
                            "group_number": 2,
                            "games_rating": [
                                {
                                    "place": 1,
                                    "player_pk": 2
                                },
                                {
                                    "place": 2,
                                    "player_pk": 6
                                },
                                {
                                    "place": 3,
                                    "player_pk": 8
                                },
                            ]
                        },
                        {
                            "group_number": 3,
                            "games_rating": [
                            {
                                "place": 1,
                                "player_pk": 7
                            },
                            {
                                "place": 2,
                                "player_pk": 3
                            },
                            {
                                "place": 3,
                                "player_pk": 4
                            }
                            ]
                        }
                    ]
            }
        }
)


swagger_schema_tournament_get_knockout = extend_schema(
        tags=["Tournament"],
        methods=["GET"],
        summary="Get tournament knockout",
        description="Get tournament knockout",
        operation_id="Get tournament knockout"
    ) 