""" Custom Swagger Serializers when usual serializer does'not compare """

# DRF imports
from rest_framework import serializers

# import serializers
from user.serializers import UserPhotoSerializer

# import models
from user.models.player import Player


class SwaggerCreatePlayerSerializer(UserPhotoSerializer):

    class Meta:
        model = Player
        fields = [
            "photo",
            "sex",
            "handedness"
        ]

    sex = serializers.CharField()
    handedness = serializers.CharField()