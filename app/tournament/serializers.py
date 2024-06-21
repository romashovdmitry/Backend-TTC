# DRF imports
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

# import models
from tournament.models.tournament import Tournament


class TournamentCreateSerializer(serializers.ModelSerializer):
    """ serializer for Tournament model create object """
    class Meta:
        model = Tournament
        fields = "__all__"
