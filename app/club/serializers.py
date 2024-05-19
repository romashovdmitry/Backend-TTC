# Python imports
import base64
from PIL import Image

# DRF imports
from rest_framework import serializers

# import models
from club.models.club import Club
from user.models.club_admin import ClubAdmin
from user.models.user import User # for annotation
from club.models.club_photoes import ClubPhoto

# import constants, config data
from club.constants import ALLOWED_IMAGE_FORMATS


class ClubPhotoSerializer(serializers.ModelSerializer):
    """
    Serializer-helper for photo serialization in
    creating new club.
    """
    class Meta:
        model = ClubPhoto
        fields = ["photo"]


class ClubUpdateSerializer(serializers.ModelSerializer):
    """
    serializer for update club info:
        - without photo field
        - without overriding create method
    """
    class Meta:
        model = Club
#        fields = "__all__"
        exclude = ["admin_club"]

    def validate_logo(self, object):
        """
        check correct format of image file or not
        """
        if object:
            image_format = Image.open(object).format

            if image_format in ALLOWED_IMAGE_FORMATS:
                return object

            raise serializers.ValidationError(
                "Image must be png, jpg or jpeg file extension"
            )

        else:
            raise serializers.ValidationError(
                "Image field is required. "
            )            


class ClubCreateSerializer(ClubUpdateSerializer):
    """
    serailizer for creating new Club object: inherited
    from ClubUpdateSerializer with ovverriding:
        - serializing club photo fields
        - create method
    """
    photo = ClubPhotoSerializer(many=True, required=False)


    # NOTE: можнz заменить на такую конструкциию
    # logo = serializers.ImageField(required=False, validators=[FileExtensionValidator(allowed_extensions=allowed_extensions)])


    def create(self, validated_data, user: User) -> Club:
        """
        redefine save method for creating club_admin
        and club photoes
        """
        photoes = self.initial_data.getlist('photo')
        validated_data = self.validated_data
        validated_data["admin_club"] = ClubAdmin.objects.create(
            user=user
        )
        club = Club.objects.create(**validated_data)

        if photoes:

            for photo_data in photoes:
                ClubPhoto.objects.create(club=club, photo=photo_data)

        return club
    

class ShowAllClubsSerializer(serializers.ModelSerializer):
    """
    serializer for returning list of user clubs
    """
    class Meta:
        model = Club
        fields = [
            "id",
            "name",
            "logo"
        ]


class ClubGetSerializer(serializers.ModelSerializer):
    """
    serializer for get info about certain club
    """
    # NOTE: в будущем надо проверить как будет возвращать значения,
    # если несколько фотографий содержит клуб и в целом как возвращает
    # фотографии
    class Meta:
        model = Club
        fields = "__all__"


