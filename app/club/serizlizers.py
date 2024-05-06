# Python imports
import base64

# DRF imports
from rest_framework import serializers

# import models
from club.models.club import Club


class ClubCreateUpdateSerializer(serializers.ModelSerializer):
    """ Serializer for creating Club instance """
    class Meta:
        model = Club
        fields = "__all__"

        logo = serializers.ImageField()

    def to_internal_value(self, data):
        image_data = data.get("logo")
        image_data = image_data.read()
        image_data_base64 = base64.b64encode(image_data).decode('utf-8')
        data["logo"] = image_data_base64

        return super().to_internal_value(data)