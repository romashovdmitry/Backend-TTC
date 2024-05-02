"""
Serializers for user operations like creating, update
user's info.
"""

# Python imports
import re

# DRF imports
from rest_framework import serializers

# Django imports
from django.db.models import Q

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
    

class UserNamesSerializer(serializers.ModelSerializer):
    """
    Serializer for user field  in
    create player JSON.
    """
    class Meta:
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


class CreateUpdatePlayerSerializer(serializers.ModelSerializer):
    """ Serializer for creating playes instance """
    user = UserNamesSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            'sex',
            'handedness',
            'rating',
            'user'
        ]

    rating = serializers.IntegerField()
