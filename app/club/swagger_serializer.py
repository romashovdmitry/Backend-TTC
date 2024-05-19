""" Custom Swagger Serializers when usual serializer does'not compare """

# DRF imports
from rest_framework import serializers

# import serializers
from user.serializers import UserPhotoSerializer

# import models
from club.models.club import Club


def define_swagger_fields_helper() -> list:
    """
    Create custom list fields for SwaggerCreateUpdateClubSerializer.
    """
    CUSTOM_FIELDS_LIST = [f.name for f in Club._meta.get_fields()]
    CUSTOM_FIELDS_LIST.append("photo")
    CUSTOM_FIELDS_LIST.remove('clubphoto')
    CUSTOM_FIELDS_LIST.remove('tournament_club')
    CUSTOM_FIELDS_LIST.remove('admin_club')
    
    return CUSTOM_FIELDS_LIST

#CUSTOM_FIELDS_LIST = [f.name for f in Club._meta.get_fields()]
#CUSTOM_FIELDS_LIST.append("photoes_field")

class SwaggerCreateUpdateClubSerializer(serializers.ModelSerializer):
    """ Serailizer for Swagger interface """
    # NOTE: instead of "__all__" because of need to add custom field
    class Meta:
        model = Club
        fields = define_swagger_fields_helper()

    photo = serializers.ListField(child=serializers.ImageField())

#        photoes_field = serializers.ImageField()

#    sex = serializers.CharField(allow_null=False, allow_blank=False)
#    handedness = serializers.CharField(allow_null=False, allow_blank=False)
