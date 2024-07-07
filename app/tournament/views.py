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
from tournament.serializers import (
    TournamentCreateSerializer,
    TournamentListSerializer,
    TournamentPlayerAddSerializer
)

# Swagger Schemas imports
from tournament.swagger_schemas import (
    swagger_schema_tournament_create,
    swagger_schema_tournament_list,
    swagger_schema_tournament_list,
    swagger_schema_admin_my_tournament_list,
    swagger_schema_add_player_to_tournament
)

# import models
from tournament.models.tournament import Tournament

# import constants
from tournament.constants import TournamentStatus

# import custom foos, classes
from main.permissions import IsClubAdmin
from telegram_bot.send_error import telegram_log_errors
from main.utils import foo_name, class_and_foo_name


class TournamentActions(ViewSet):
    """ class for creating and updating clubs """
    http_method_names = ['post', 'put', 'get', 'delete']
    lookup_field = 'id'
    permission_classes = [IsClubAdmin, IsAuthenticated]

    serializer_map = {
        'create_tournament': TournamentCreateSerializer,
        "list_tournament": TournamentListSerializer,
        "list_my_tournaments": TournamentListSerializer,
        "add_player_to_tournament": TournamentPlayerAddSerializer
    }

    permission_map = {
        "create_tournament": [IsClubAdmin],
        "list_my_tournaments": [IsClubAdmin],
        "list_tournament": [IsAuthenticated]
    }

    def get_permissions(self):
        """ Return the permissions based on the action """
        try:

            return [permission() for permission in self.permission_map[self.action]]

        except KeyError:

            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        """ define serializer for class """

        return self.serializer_map[self.action]

    def get_queryset(self):
        """ define queryset for class """

        if self.action == "list_tournament":
        
            return Tournament.objects.filter(
                    status=TournamentStatus.CONFIGURED
                ).all()

        if self.action == "list_my_tournaments":

            return Tournament.objects.filter(
                    club=self.club_pk
                ).all()

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
#                     user=request.user
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

    @swagger_schema_tournament_list
    @action(
        detail=False,
        methods=['get'],
        url_path="list_tournament",
    )
    def list_tournament(self, request) -> Response:

        try:
            queryset = self.get_queryset()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            serializer_data = serializer.data

            return Response(status=200, data=serializer_data)

        except Exception as ex:

            asyncio.run(
                telegram_log_errors(
                    f"[{class_and_foo_name()}] {str(ex)}"
                )
            )
            
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST,
            )

    @swagger_schema_admin_my_tournament_list
    @action(
        detail=False,
        methods=['get'],
        url_path="list_my_tournaments",
    )
    def list_my_tournaments(
        self,
        request,
        club_pk=None
    ) -> Response:

        try:
            self.club_pk = club_pk
            queryset = self.get_queryset()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=True)
            serializer_data = serializer.data

            return Response(status=200, data=serializer_data)

        except Exception as ex:

            asyncio.run(
                telegram_log_errors(
                    f"[{class_and_foo_name()}] {str(ex)}"
                )
            )
            
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST,
            )
        
    @swagger_schema_add_player_to_tournament
    @action(
        detail=False,
        methods=["put"],
        url_path="add_player_to_tournament"
    )
    def add_player_to_tournament(
        self,
        request
    ) -> Response:

        try:
            serializer = self.get_serializer_class()
            serializer = serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.create(
                    validated_data=serializer.validated_data,
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