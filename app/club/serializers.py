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


class ClubCreateUpdateSerializer(serializers.ModelSerializer):
    """ serailizer for creating new Club object """
    photo = ClubPhotoSerializer(many=True, required=False)

    class Meta:
        model = Club
        fields = "__all__"

    # NOTE: можнz заменить на такую конструкциию
    # logo = serializers.ImageField(required=False, validators=[FileExtensionValidator(allowed_extensions=allowed_extensions)])
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

    def create(self, validated_data, user: User) -> Club:
        """
        redefine save method for creating club_admin
        and club photoes
        """
        print(1)
        photoes = self.initial_data.get('photo')
        print(2)
        print(validated_data)
        club = Club.objects.create(**validated_data)
        print(3)
        if photoes:
            print(4)
            for photo_data in photoes:
                photo = ClubPhoto.objects.create(club=club, photo=photo_data)
                photo.save()
                print(5)
        print(6)
        club_admin = ClubAdmin.objects.create(
            user=user
        )
        print(7)
        club.admin_club = club_admin
        club.save()

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
