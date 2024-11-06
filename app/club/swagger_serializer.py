"""
Custom Swagger Serializers when usual serializer does'not compare .
Use it when send images to backend from Swagger. 
"""

# DRF imports
from rest_framework import serializers

# import serializers
from user.serializers import UserPhotoSerializer

# import models
from club.models.club import Club


def define_swagger_fields_helper() -> list:
    """
    Create custom list fields for SwaggerCreateUpdateClubPhotoSerializer.
    """
    CUSTOM_FIELDS_LIST = [f.name for f in Club._meta.get_fields()]
    CUSTOM_FIELDS_LIST.append("photo")
#    CUSTOM_FIELDS_LIST.remove('club_photo')
    CUSTOM_FIELDS_LIST.remove('tournament_club')
    CUSTOM_FIELDS_LIST.remove('admin_club')
    CUSTOM_FIELDS_LIST.remove('is_active')
    # DELETEME: it's only for tests on local! 
    # on prod we need photoes
    CUSTOM_FIELDS_LIST.remove('logo')

    return CUSTOM_FIELDS_LIST

#CUSTOM_FIELDS_LIST = [f.name for f in Club._meta.get_fields()]
#CUSTOM_FIELDS_LIST.append("photoes_field")


class SwaggerCreateUpdateClubPhotoSerializer(serializers.ModelSerializer):
    """ Serailizer for Swagger interface """
    # NOTE: instead of "__all__" because of need to add custom field
    class Meta:
        model = Club
        fields = define_swagger_fields_helper()

    photo = serializers.ListField(child=serializers.ImageField())
