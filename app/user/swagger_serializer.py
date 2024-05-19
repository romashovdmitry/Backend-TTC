""" Custom Swagger Serializers when usual serializer does'not compare """

# DRF imports
from rest_framework import serializers

# import serializers
from user.serializers import UserPhotoSerializer

# import models
from user.models.player import Player


class SwaggerCreatePlayerSerializer(UserPhotoSerializer):
    """ Serializer for Swagger interface """

    class Meta:
        model = Player
        fields = [
            "photo",
            "sex",
            "handedness",
            "blade",
            "rubber_forehand",
            "rubber_backhand"
        ]


class SwaggerUpdatePlayerSerializer(SwaggerCreatePlayerSerializer):
    """ Serializer for Swagger interface """

    photo = serializers.ImageField(required=False, allow_null=True)
