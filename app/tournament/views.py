""" это наперёд закинул сразу.  """

# Django imports
from django.shortcuts import get_object_or_404

# DRF imports
from rest_framework.viewsets import ViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

# Swagger imports
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes

# import models
from club.models.club import Club

# import constants, config data
from club.constants import OPENING_HOURS_SWAGGER_EXAMPLE

# import serializers
from club.serializers import (
    ClubCreateUpdateSerializer,
    ShowAllClubsSerializer,
    ClubGetSerializer
)
