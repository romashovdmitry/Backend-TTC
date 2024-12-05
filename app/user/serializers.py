"""
Serializers for user operations like creating, update
user's info.
"""

# Python imports
import re
import asyncio

# DRF imports
from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError

# Swagger imports
from drf_spectacular.utils import extend_schema_serializer

# import models
from user.models import (
    User,
    Player,
    PlayerRatingHistory
)

# import constants
from user.constants import (
    GET_INFO_ABOUT_USER_RETURN_DICT,
    GenderChoise,
    GeoChoiсe
)

# import custom foos
from user.services import hashing
from user.utils import create_date_for_json_to_frontend


class CreateUserSerializer(serializers.ModelSerializer):
    ''' Serizlizer for creating user instance '''

    class Meta:
        model = User
        fields = [
            'email',
            'password',
            'first_name',
            'second_name',
            "sex",
            'birth_date'
        ]
        # https://stackoverflow.com/a/66790239/24040439
        extra_kwargs = {i:{'required': True, "allow_null": False} for i in fields}

    email = serializers.EmailField(
        trim_whitespace=True,
        label='Email'
    )

    password = serializers.CharField(
        trim_whitespace=True,
        label='Password'
    )

    def validate_first_name(self, first_name_string: str) -> str | serializers.ValidationError:
        """
        Validate length of first_name string
        """
        if len(first_name_string) < 3:
            raise serializers.ValidationError(
                "First Name must contains at least 2 alphabets",
                code="fist_name_too_short"
            )
        return first_name_string
    
    def validate_second_name(self, second_name_string: str) -> str | serializers.ValidationError:
        """
        Validate length of second_name string        
        """
        if len(second_name_string) < 3:
            raise serializers.ValidationError(
                "Last Name must contains at least 2 alphabets",
                code="second_name_too_short"
            )
        return second_name_string            

    def validate_password(self, password):
        ''' validate password '''
#        if not any(char.isdigit() for char in password):
#            raise serializers.ValidationError(
#                "Password must contain at least one digit.",
#                code="password_no_digit"
#            )

#        if not any(char.isupper() for char in password):
#            raise serializers.ValidationError(
#                "Password must contain at least one uppercase letter.",
#                code="password_no_uppercase"
#            )

#        if not any(char.islower() for char in password):
#            raise serializers.ValidationError(
#                "Password must contain at least one lowercase letter.",
#                code="password_no_lowercase"
#            )
#        if len(password) < 7:
#            raise serializers.ValidationError(
#                "Password must be at least 7 characters long.",
#                code="password_length"
#            )
        if len(password) > 20:
            raise serializers.ValidationError(
                "Password must be at most 20 characters long.",
                code="password_length"
            )

        return password

    def validate_email(self, email):
        ''' validate email unique '''
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "email already exists",
                code='email_exists'
            )

        return email


class LoginUserSerializer(CreateUserSerializer):
    ''' serializer for get objects of Product model'''

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
        # https://stackoverflow.com/a/66790239/24040439
        extra_kwargs = {i:{'required': True, "allow_null": False} for i in fields}


    def validate_email(self, email):
        """
        Redefine because we don't need check email on
        exists or not.
        """
        return email

    def validate_password(self, password):
        """
        Redefine to check is password
        correct or wrong.
        """
        try:
            super().validate_password(password)

        except exceptions.ValidationError as ex:
            raise serializers.ValidationError(ex)

        email = self.initial_data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            if asyncio.run(
                hashing(
                    password
                )
            ) == user.password:

                return password

            raise serializers.ValidationError("Invalid password")

        raise serializers.ValidationError("There is no user with this email or username")


class UserNamesSerializer(serializers.ModelSerializer):
    """
    Serializer for user field in
    create player JSON.
    """
    class Meta:
        model = User
        fields = [
            "first_name",
            "second_name"
        ]
    
    first_name = serializers.CharField(
        trim_whitespace=True
    )
    second_name = serializers.CharField(
        trim_whitespace=True,
    )


class UserPhotoSerializer(serializers.ModelSerializer):
    """
    Serializer-helper for photo serialization in
    creating new player.
    """
    class Meta:
        model = User
        fields = ("photo",)

    photo = serializers.ImageField()


class UpdatePlayerSerializer(serializers.ModelSerializer):
    """ Serializer for creating player instance """
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships

    geo = serializers.ChoiceField(choices=GeoChoiсe, write_only=True)

    class Meta:
        model = Player
        exclude = ["photo", "user"]

    def update(self, instance, validated_data):
        geo = validated_data.pop("geo", None)
        instance = super().update(instance, validated_data)

        if geo is not None:
            instance.user.geo = geo
            instance.user.save()

        return instance


# FIXME: это можно сделать, уверен, через два сериалайзера
# вместо переопределения метода create
class CreatePlayerSerializer(UpdatePlayerSerializer):
    """ Serializer for creating player instance """
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships

#    photo = serializers.ImageField(required=False)

    def create(self, validated_data: dict, user: User):
#        photo = validated_data.pop("photo")
        validated_data["user_id"] = user.id

        # if player does not exists
        if Player.objects.filter(
            user=self.initial_data["user"]
        ).first() is None:
            player = Player.objects.create(**validated_data)

#            if photo:
#                user.photo = photo
#                user.save()

            return player
    
        raise ValidationError("Player already created!")

    
class UpdateCreatePlayerPhotoSerializer(serializers.ModelSerializer):
    """ Serializer for creating player instance """
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships

    class Meta:
        model = Player
        fields = ["photo"]

    photo = serializers.ImageField(required=False)


class GetPlayerInfoSerializer(serializers.ModelSerializer):
    """ serializer for returning info aout Playser by user.id """
    class Meta:
        model = Player
        fields = "__all__"

    def to_representation(self, instance: Player):
        """
        from back to front
        """
        try:
            rating_created_at_list = PlayerRatingHistory.objects.filter(
                    player=instance
                ).values_list(
                    "created",
                    "actual_rating"
                )

            GET_INFO_ABOUT_USER_RETURN_DICT["id"] = instance.pk

            GET_INFO_ABOUT_USER_RETURN_DICT["info"]["first_name"] = \
                instance.user.first_name
            GET_INFO_ABOUT_USER_RETURN_DICT["info"]["second_name"] = \
                instance.user.second_name
            GET_INFO_ABOUT_USER_RETURN_DICT["info"]["email"] = \
                instance.user.email
            GET_INFO_ABOUT_USER_RETURN_DICT["info"]["birthday"] = \
                create_date_for_json_to_frontend(
                    instance.user.birth_date
                )
            GET_INFO_ABOUT_USER_RETURN_DICT["info"]["photo"] = \
                instance.photo.url if instance.photo else None
            GET_INFO_ABOUT_USER_RETURN_DICT["info"]["sex"] = \
                GenderChoise(int(instance.user.sex)).label

            GET_INFO_ABOUT_USER_RETURN_DICT["community"]["geo"] = \
                instance.user.geo
            GET_INFO_ABOUT_USER_RETURN_DICT["community"]["playing_hand"] = \
                instance.playing_hand
            GET_INFO_ABOUT_USER_RETURN_DICT["community"]["racket"]["blade"] = \
                instance.blade
            GET_INFO_ABOUT_USER_RETURN_DICT["community"]["racket"]["rubber_forehand"] = \
                instance.rubber_forehand
            GET_INFO_ABOUT_USER_RETURN_DICT["community"]["racket"]["rubber_backhand"] = \
                instance.rubber_backhand

            GET_INFO_ABOUT_USER_RETURN_DICT["rating"]["dates"] = [
                create_date_for_json_to_frontend(elem_tuple[0])
                for elem_tuple in rating_created_at_list
            ]
            GET_INFO_ABOUT_USER_RETURN_DICT["rating"]["data"] = [
                elem_tuple[1] for elem_tuple in rating_created_at_list
            ]

            return GET_INFO_ABOUT_USER_RETURN_DICT

        except exceptions.ValidationError as ex:

            raise serializers.ValidationError(ex)


class GetPeriodicalPlayerRating(serializers.ModelSerializer):
    """ serializer for returing data about updates in player's rating """

    class Meta:
        model = PlayerRatingHistory
        exclude = ("player", "id",)
