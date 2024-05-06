# Python imports
import json
import asyncio

# Django imports
from django.http import HttpResponse

# DRF imports
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

# Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from club.serizlizers import ClubCreateUpdateSerializer


class ClubCreateUpdate(ViewSet):
    """ class for creating and updating clubs """
    parser_classes = (MultiPartParser,)
    http_method_names = ['post', 'patch']
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """ define serializer for class """
        if self.action == 'create_club':
            return ClubCreateUpdateSerializer

    @swagger_auto_schema(
        tags=["Club"],
        operation_id="Create Club",
        operation_description="POST request to create new club",
        method="POST",
        # NOTE: use manual becase of i didn't find way to use
        # and manual and request_body parameter. And didn't find
        # way to add file uploading field by request_body.  
        # https://stackoverflow.com/questions/63068565/drf-yasg-custom-json-body
        # https://stackoverflow.com/questions/57382779/how-to-make-swagger-schema-for-file-upload-api-in-django-rest-framework-using-dr
        # https://github.com/axnsan12/drf-yasg/issues/767
        # https://github.com/axnsan12/drf-yasg/issues/600
        manual_parameters=[
            openapi.Parameter(
                name="name",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Official name of the club"
            ),
            openapi.Parameter(
                name="logo",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=False,
                description="Club logo in file format"
            ),
            openapi.Parameter(
                name="club_photoes",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_FILE
                ),
                required=False,
                description="Club photoes"
            ),
            openapi.Parameter(
                name="state",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="State where the club is located"
            ),
            openapi.Parameter(
                name="city",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="City where the club is located"
            ),
            openapi.Parameter(
                name="address",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Street address of the club"
            ),
            openapi.Parameter(
                name="phone_number",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Phone number of the club"
            ),
            openapi.Parameter(
                name="opening_hours",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Days and hours when the club is open"
            ),
            openapi.Parameter(
                name="about",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Additional information about the club"
            ),
            openapi.Parameter(
                name="social_link",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description="Link to the club's social network page"
            ),
            openapi.Parameter(
                name="link",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description="Link to the club's website"
            )
        ],
    )
    @action(
        detail=False,
        methods=['post'],
        url_path="create_club",
        parser_classes=(MultiPartParser,)
    )
    def create_club(self, request) -> Response:
        """
        1. Creating new Club instance.
        2. Create new Admin Club instance, linked to user.
        """
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            instance = serializer.save()
            # go to hash password
            instance.save()
            return Response(
                status=HTTP_201_CREATED                
            )

        else:

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Club"],
        operation_id="Update Club",
        operation_description="Patch request to update existing club",
        method="PATCH",
        # NOTE: use manual becase of i didn't find way to use
        # and manual and request_body parameter. And didn't find
        # way to add file uploading field by request_body.  
        # https://stackoverflow.com/questions/63068565/drf-yasg-custom-json-body
        # https://stackoverflow.com/questions/57382779/how-to-make-swagger-schema-for-file-upload-api-in-django-rest-framework-using-dr
        # https://github.com/axnsan12/drf-yasg/issues/767
        # https://github.com/axnsan12/drf-yasg/issues/600
        manual_parameters=[
            openapi.Parameter(
                name="name",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="Official name of the club"
            ),
            openapi.Parameter(
                name="Logo",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=False,
                description="Club logo in file format"
            ),
            openapi.Parameter(
                name="club_photoes",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_FILE
                ),
                required=False,
                description="Club photoes"
            ),
            openapi.Parameter(
                name="state",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="State where the club is located"
            ),
            openapi.Parameter(
                name="city",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="City where the club is located"
            ),
            openapi.Parameter(
                name="address",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Street address of the club"
            ),
            openapi.Parameter(
                name="phone_number",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Phone number of the club"
            ),
            openapi.Parameter(
                name="opening_hours",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Days and hours when the club is open"
            ),
            openapi.Parameter(
                name="about",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Additional information about the club"
            ),
            openapi.Parameter(
                name="social_link",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description="Link to the club's social network page"
            ),
            openapi.Parameter(
                name="link",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_URI,
                description="Link to the club's website"
            )
        ],
    )
    @action(
        detail=False,
        methods=['patch'],
        url_path="update_club"
    )
    def update_club(self, request) -> Response:
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            instance = serializer.save()
            # go to hash password
            instance.save()
            return Response(
                status=HTTP_201_CREATED                
            )

        else:

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

