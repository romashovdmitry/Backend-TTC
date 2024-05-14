"""
Serializers for user operations like creating, update
user's info.
"""

# Python imports
import re
import asyncio

# DRF imports
from rest_framework import serializers, exceptions

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
            'last_name',
            'birth_date'
        ]

    email = serializers.EmailField(
        trim_whitespace=True,
        label='Email'
    )

    password = serializers.CharField(
        trim_whitespace=True,
        label='Password'
    )

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
            "last_name"
        ]
    
    first_name = serializers.CharField(
        trim_whitespace=True
    )
    last_name = serializers.CharField(
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


# FIXME: это можно сделать, уверен, через два сериалайзера
# вместо переопределения метода create
class CreateUpdatePlayerSerializer(serializers.ModelSerializer):
    """ Serializer for creating player instance """
    # https://www.django-rest-framework.org/api-guide/relations/#nested-relationships

    class Meta:
        model = Player
        fields = [
            'sex',
            'handedness',
            'rating',
            'photo'
        ]

    photo = serializers.ImageField()

    def create(self, validated_data: dict, user: User):
        print('go 0')
        print(validated_data)
        print(type(validated_data))
        photo = validated_data.pop("photo")
        player = Player.objects.create(**validated_data)
        print('go 1')
        if photo:
            print('go 2')
            user.photo = photo
            print('go 3')
            user.save()
            print('go 4')
        return player