"""
tounament views actions:
- create tournament
- get info about tournament
"""
# Python imports
import asyncio

# Django imports
from django.shortcuts import get_object_or_404

# DRF imports
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

# Serializers imports
from tournament.serializers import TournamentCreateSerializer

# Swagger Schemas imports
from tournament.swagger_schemas import swagger_schema_tournament_create

# import models
from tournament.models.tournament import Tournament

# import constants
# import custom foos, classes
from main.permissions import IsClubAdmin
from telegram_bot.send_error import telegram_log_errors


class TournamentActions(ViewSet):
    """ class for creating and updating clubs """
    http_method_names = ['post', 'put', 'get', 'delete']
    lookup_field = 'id'
    permission_classes = [IsClubAdmin]
    queryset = Tournament.objects.all()

    serializer_map = {
        'create_tournament': TournamentCreateSerializer
    }

    def get_serializer_class(self):
        """ define serializer for class """

        return self.serializer_map[self.action]

    @swagger_schema_tournament_create
    @action(
        detail=False,
        methods=['post'],
        url_path="create_tournament",
    )
    def create_tournament(self, request) -> Response:
        """
        Creating new Tournament instance
        """
        try:
            serializer = self.get_serializer_class()
            serializer = serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.create(
                    validated_data=serializer.validated_data,
                    user=request.user
                )
                return Response(status=HTTP_201_CREATED)

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[TournamtneActions][create_tournament] {str(ex)}"
                )
            )
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST
            )