# Python imports
import base64
import re
from PIL import Image

# asyncio imports
import asyncio

# DRF imports
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# import models
from club.models.club import Club
from user.models.club_admin import ClubAdmin
from user.models.user import User # for annotation
from club.models.club_photoes import ClubPhoto
from tournament.models import Tournament

# import constants, config data
from club.constants import ALLOWED_IMAGE_FORMATS

# import custom foos, classes
from telegram_bot.send_error import telegram_log_errors
from main.utils import class_and_foo_name, foo_name
from club.utils import (
    create_tournament_date_for_json_to_frontend,
    create_tournament_time_for_json_to_frontend
)


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
        exclude = ["admin_club", "logo"]

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

    def create(self, validated_data, user: User) -> Club:
        """
        redefine save method for creating club_admin
        and club photoes
        """
#        photoes = self.initial_data.getlist('photo')
        validated_data = self.validated_data
        validated_data["admin_club"] = ClubAdmin.objects.create(
            user=user
        )
        club = Club.objects.create(**validated_data)

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

    def to_representation(self, instance: Club):
        """
        FIXME: in Enlish
        переопределяем для разделения строки на массивы
        по требованию фронта.
        """
        try:
            return_representation = super().to_representation(instance)

            about = return_representation.get("about", "")
            about = re.split(r'(\n|\s+)', about)
            about = [
                elem.replace('\n\n', '\n').replace(' ', '')
                for elem
                in about
                if elem != ' '
            ]
            
            return_representation["about"] = about

            if hasattr(instance, 'club_photoes') and instance.club_photoes.exists():
                return_representation["photoes"] = [
                    photo_object.photo.url
                    for photo_object
                    in instance.club_photoes.all()
                ]

            else:
                return_representation["photoes"] = None

            for x in instance.club_tournaments.all():
                create_tournament_date_for_json_to_frontend(
                    x.date_time
                )
                create_tournament_time_for_json_to_frontend(
                    x.date_time
                )

            return_representation["upcoming"] = [
                    {
                        "id": club_tournament.pk,
                        "name": club_tournament.name,
                        "date": create_tournament_date_for_json_to_frontend(
                            club_tournament.date_time
                        ),
                        "time": create_tournament_time_for_json_to_frontend(
                            club_tournament.date_time
                        ),
#                        "url": "/"
                    }
                    for club_tournament
                    in instance.club_tournaments.all()
                    if int(club_tournament.status) in [0,1]
            ]

            return return_representation

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[{class_and_foo_name()}][{foo_name()}] {str(ex)}"
                )
            )

            raise ValidationError(
                detail="There is an error. ",
                code="not_validated_data"
            )