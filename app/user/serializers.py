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
from user.models.user import User
from user.models.player import Player

# import custom foos
from user.services import hashing


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
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                "Password must contain at least one digit.",
                code="password_no_digit"
            )

        if not any(char.isupper() for char in password):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter.",
                code="password_no_uppercase"
            )

        if not any(char.islower() for char in password):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter.",
                code="password_no_lowercase"
            )
        if len(password) < 7:
            raise serializers.ValidationError(
                "Password must be at least 7 characters long.",
                code="password_length"
            )
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

    class Meta:
        model = Player
        exclude = ["photo"]

#    photo = serializers.ImageField(required=False)


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