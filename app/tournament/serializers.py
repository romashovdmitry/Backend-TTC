# DRF imports
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

# import models
from tournament.models import (
    Tournament,
    TournamentPlayers
)
from club.models.club import Club


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