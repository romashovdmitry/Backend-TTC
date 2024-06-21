# Swagger imports
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes


swagger_schema_tournament_create = extend_schema(
        tags=["Tournament"],
        summary="Create new Tournament",
        description="POST request to create new Tournament",
        operation_id="Create new Tournament",
        request={
            "application/json": {
                "description": "New tournament in club created by club admin",
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "date_time": {
                        "type": "string",
                    },
                    "max_players_amount": {
                        "type": "integer"
                    },
                    "min_rating_limit": {
                        "type": "integer"
                    },
                    "max_rating_limit": {
                        "type": "integer"
                    },
                    "club": {
                        "type": "integer"
                    }
                },
                "required": [
                    "name",
                    "date_time",
                    "max_players_amount",
                    "min_rating_limit",
                    "max_rating_limit",
                    "club"
                ],
            }
        },
    )