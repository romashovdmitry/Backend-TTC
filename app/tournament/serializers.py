# Python imports
import asyncio

# DRF imports
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

# Django imports
from django.db.models import F

# import models
from tournament.models import (
    Tournament,
    TournamentPlayers,
    Game
)
from club.models.club import Club

# import constants
from tournament.constants import GameStatus

# import custom foos, classes
from telegram_bot.send_error import telegram_log_errors
from main.utils import class_and_foo_name, foo_name

class TournamentCreateSerializer(serializers.ModelSerializer):
    """ serializer for Tournament model create object """

    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all())

    class Meta:
        model = Tournament
        fields = [
            "name",
            "date_time",
            "player_pyament",
            "club"
        ]


class TournamentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = "__all__"


class TournamentPlayerAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = TournamentPlayers
        fields = "__all__"


class TournamentCreateGroupsSerializer(serializers.ModelSerializer):
    """ Serializer for POST request that divide players on groups """
    class Meta:
        model = Tournament
        fields = [
            "group_number",
            "group_players_number",
            "group_qualifiers_number"
        ]        

    def validate(self, attrs):
        try:
            attrs = super().validate(attrs)
            tournament_pk = self.initial_data.get("tournament_pk")

            if tournament_pk:
                attrs = super().validate(attrs)
    
            else:
                raise ValidationError(
                    detail="There is no tournament pk in request",
                    code="no_tournament_pk"
                )

            group_players_number = attrs.get("group_players_number")
            group_number = attrs.get("group_number")

            if not group_players_number and not group_number:
                raise ValidationError(
                    detail=(
                        "At least one of group_players_number "
                        "or group_number must be provided"
                    ),
                    code="missing_fields"
                )

            # FIXME: на этом этапе разводить игроков по реитингу. 
            tournament_players = TournamentPlayers.objects.filter(
                tournament=Tournament.objects.get(
                    pk=tournament_pk
                )
            ).all()

            tournament_players = TournamentPlayers.objects.filter(
                tournament=Tournament.objects.get(pk=tournament_pk)
            ).annotate(
                player_rating=F('player__rating')  # Добавляем рейтинг игрока как аннотированное поле
            ).order_by('-player_rating')  # Сортируем по рейтингу

            empty_list = [None] * len(tournament_players)

            start = 0
            end = len(empty_list) - 1

            for idx, tp in enumerate(tournament_players):

                if idx % 2 == 0:
                    empty_list[start] = tp
                    start += 1

                else:
                    empty_list[end] = tp
                    end -= 1

            attrs['tournament_players'] = tournament_players
            attrs['tournament_pk'] = tournament_pk

            return attrs

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[{class_and_foo_name()}][{foo_name()}] {str(ex)}"
                )
            )

            raise ValidationError(
                detail="Not validated data. Please, check out that",
                code="not_validated_data"
            )
 
    def save(self):
        return_ = self.validated_data.copy()
        # FIXME: это велосипед.
        self.validated_data.pop("tournament_players")
        self.validated_data.pop("tournament_pk")
        super().save()

        return return_
    

class GameStartSerializer(serializers.ModelSerializer):
    """
    Serializer for data to fix game started.
    """
    class Meta:
        model = Game
        fields = [
            "pk",
            "tournament"
        ]
    
    def save(self: Game, **kwargs: dict):
        """
        ovverride save method to define save behavior. 
        """
        self.instance.status = GameStatus.STARTED

        return super().save(**kwargs)


class GameResultSerializer(GameStartSerializer):
    """
    Serializer for data with game's result
    """
    class Meta:
        exclude = [
            "order",
            "first_player",
            "second_player"
        ]
