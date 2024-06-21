""" Custom Swagger Serializers when usual serializer does'not compare """

# DRF imports
from rest_framework import serializers

# import serializers
from user.serializers import UserPhotoSerializer

# import models
from user.models.player import Player


class SwaggerUpdatePlayerSerializer(UserPhotoSerializer):
    """ Serializer for Swagger interface """

    class Meta:
        model = Player
        fields = [
            "playing_hand",
            "blade",
            "rubber_forehand",
            "rubber_backhand"
        ]


class SwaggerCreateUpdatePlayerPhotoSerializer(UserPhotoSerializer):
    """ Serializer for Swagger interface """

    class Meta:
        model = Player
        fields = [
            "photo",
        ]

    photo = serializers.ImageField(required=False, allow_null=True)
