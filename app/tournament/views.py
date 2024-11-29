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
    TournamentPlayerAddSerializer,
    TournamentCreateGroupsSerializer,
    GameStartSerializer,
    GameResultSerializer
)

# Swagger Schemas imports
from tournament.swagger_schemas import (
    swagger_schema_tournament_create,
    swagger_schema_tournament_list,
    swagger_schema_tournament_list,
    swagger_schema_admin_my_tournament_list,
    swagger_schema_add_player_to_tournament,
    swagger_schema_game_start,
    swagger_schema_game_result,
    swagger_schema_create_groups,
    swagger_schema_get_info_about_tournament_by_pk,
    swagger_schema_get_groups,
    swagger_schema_create_groups_game_rating
)

# import models
from tournament.models import Tournament
from tournament.models import Game

# import constants
from tournament.constants import TournamentStatus

# import custom foos, classes
from main.permissions import IsClubAdmin
from telegram_bot.send_error import telegram_log_errors
from main.utils import foo_name, class_and_foo_name
from tournament.services import (
    divide_players_to_groups,
    create_tournament_games,
    create_tournament_grid,
    get_tournament_grid,
    create_groups_game_rating
)


class TournamentActions(ViewSet):
    """ class for creating and updating clubs """
    http_method_names = ['post', 'put', 'get', 'delete']
    lookup_field = 'id'
    permission_classes = [IsClubAdmin, IsAuthenticated]

    serializer_map = {
        'create_tournament': TournamentCreateSerializer,
        "list_tournament": TournamentListSerializer,
        "list_my_tournaments": TournamentListSerializer,
        "add_player_to_tournament": TournamentPlayerAddSerializer,
        "create_groups": TournamentCreateGroupsSerializer,
        # NOTE: сюда тоже подойдёт, хоть и pk
        "get_info_about_tournament_by_pk": TournamentListSerializer
    }

    permission_map = {
        "create_tournament": [IsClubAdmin],
        "create_groups": [IsClubAdmin],
        "list_my_tournaments": [IsClubAdmin],
        "list_tournament": [IsAuthenticated],
        "get_info_about_tournament_by_pk": [IsAuthenticated]
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

    def get_queryset(self, **kwargs):
        """ define queryset for class """

        if self.action == "list_tournament":
        
            return Tournament.objects.filter(
                    status=TournamentStatus.CONFIGURED
                ).all()

        # NOTE: пока никак не исполоьзуется.
        elif self.action == "list_my_tournaments":

            return Tournament.objects.filter(
                    club=self.club_pk
                ).all()

        elif self.action == "create_groups":
            
            # FIXME NOTE: судя по всему не используется
            return Tournament.objects.filter(
                pk=kwargs["tournament_pk"]
            ).first()

        elif self.action in [
            "get_info_about_tournament_by_pk",
            "create_groups_game_rating"
        ] :

            return Tournament.objects.filter(
                pk=kwargs["tournament_pk"]
            ).first()

    @swagger_schema_get_info_about_tournament_by_pk
    def get_info_about_tournament_by_pk(
            self,
            request,
            tournament_pk=None
    ) -> Response:

        try:
            queryset = self.get_queryset(tournament_pk=tournament_pk)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(queryset, many=False)
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
    @swagger_schema_create_groups
    @action(
        detail=False,
        methods=["put"],
        url_path="create_groups"
    )
    def create_groups(
            self,
            request,
            tournament_pk=None,
    ) -> Response:
        """
        Divide players into groups.
        """
        try:
            serializer = self.get_serializer_class()
            request.data["tournament_pk"] = tournament_pk
            # NOTE: добавить проверку на наличие уже разбитых игр ???
            serializer = serializer(data=request.data)
    
            if serializer.is_valid(raise_exception=True):
                serializer_saved_data = serializer.save()
                divide_players_to_groups_bool, \
                    serializer_saved_data["group_number"] = asyncio.run(
                        divide_players_to_groups(
                            **serializer_saved_data
                        )
                    )

                if divide_players_to_groups_bool:
                    bool_, games_dict = create_tournament_games(**serializer_saved_data)

                    if bool_:
                        tournament_grid: dict = create_tournament_grid(
                            games_dict=games_dict,
                            **serializer_saved_data
                        )

                        return Response(
                            status=HTTP_201_CREATED,
                            data=tournament_grid
                        )

                    else:

                        return Response(
                            status=HTTP_400_BAD_REQUEST,
                            data="There is and unexpected error"
                        )
    
                else:

                    return Response(
                        status=HTTP_400_BAD_REQUEST,
                        data="There is and unexpected error"
                    )

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

    @swagger_schema_create_groups_game_rating
    @action(
        detail=True,
        methods=["post"],
        url_path="create_groups_game_rating"
    )
    def create_groups_game_rating(
            self,
            request,
            tournament_pk=None,
    ) -> Response:
        """
        похую сеичас
        """
        try:
            request.data["tournament_pk"] = tournament_pk
            print('come to view, go to create jnockout games')
            created_knockout_games = create_groups_game_rating(
                self.get_queryset(
                    tournament_pk=tournament_pk
                )
            )
            print(f'created_knockout_games -> {created_knockout_games}')
            return Response(
                status=HTTP_200_OK,
                data=created_knockout_games
            )

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


    @swagger_schema_get_groups
    @action(
        detail=True,
        methods=["get"],
        url_path="get_groups"
    )
    def get_groups(
            self,
            request,
            tournament_pk=None,
    ) -> Response:
        """
        Get tournament's groups
        """
        try:
            tournament_object = Tournament.objects.filter(pk=tournament_pk).first()

            if tournament_object:

                tournament_grid = get_tournament_grid(tournament_object)

                return Response(
                    status=HTTP_200_OK,
                    data=tournament_grid
                )

            else:

                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    data="There is no tournament."
                )

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


class GameActions(ViewSet):
    """ class for creating and updating tournament's games """
    http_method_names = ['post', 'put', 'get', 'delete']
    permission_classes = [IsClubAdmin]

    serializer_map = {
        "game_result": GameResultSerializer,
        "game_start": GameStartSerializer
    }

    def get_serializer_class(self):
        """ define serializer for class """

        return self.serializer_map[self.action]

    def get_queryset(self, **kwargs):
        """ define queryset for class """

        if self.action in [
            "game_start",
            "game_result"
        ]:
        
            return Game.objects.filter(
                    pk=kwargs["game_pk"]
                ).first()

    @swagger_schema_game_start
    @action(
        detail=True,
        methods=["put"],
        url_path="create_groups"
    )
    def game_start(
            self,
            request,
            game_pk=None
    ):
            """ To mark the game as started """
            try:
                serializer = self.get_serializer_class()
                queryset = self.get_queryset(game_pk=game_pk)
                request.data["pk"] = game_pk
                serializer = serializer(queryset, data=request.data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    return Response(status=HTTP_200_OK)

                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    data="There is and unexpected error"
                )

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
            
    @swagger_schema_game_result
    @action(
        detail=True,
        methods=['put'],
        url_path="game_result"
    )
    def game_result(
        self,
        request,
        game_pk=None
    ):
        """ To save game result """
        try:
            serializer = self.get_serializer_class()
            queryset = self.get_queryset(game_pk=game_pk)
            request.data["pk"] = game_pk
            serializer = serializer(queryset, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return Response(status=HTTP_200_OK)

            return Response(
                status=HTTP_400_BAD_REQUEST,
                data="There is and unexpected error"
            )

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