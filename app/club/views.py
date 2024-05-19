# Python imports
import asyncio

# DRF imports
from rest_framework.views import View
from rest_framework.viewsets import ViewSet
from rest_framework.generics import (
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED
)

# Swagger imports
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse
)

from drf_spectacular.types import OpenApiTypes

# import models
from club.models.club import Club
from club.models.club_photoes import ClubPhoto

# import constants, config data
from club.constants import OPENING_HOURS_SWAGGER_EXAMPLE

# import serializers
from club.serializers import (
    ClubCreateSerializer,
    ClubUpdateSerializer,
    ShowAllClubsSerializer,
    ClubGetSerializer,
    ClubPhotoSerializer
)
from club.swagger_serializer import SwaggerCreateUpdateClubSerializer

# import custom foos, classes, etc
from telegram_bot.send_error import telegram_log_errors
from club.utils import define_club_of_user


class ClubActions(ViewSet, RetrieveAPIView):
    """ class for creating and updating clubs """
    parser_classes = (MultiPartParser,)
    http_method_names = ['post', 'put', 'get', 'delete']
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = Club.objects.all()

    serializer_map = {
        'create_club': ClubCreateSerializer,
        'update_club': ClubUpdateSerializer,
        'list_clubs': ShowAllClubsSerializer,
        'get_club': ClubGetSerializer,
    }

    def get_serializer_class(self):
        """ define serializer for class """

        return self.serializer_map[self.action]

    @extend_schema(
        tags=["Club"],
        summary="Create new Club",
        description="POST request to create new club",
        operation_id="Create new club",
        request=SwaggerCreateUpdateClubSerializer,
        examples=[
            OpenApiExample(
                'Example: opennings hours',
                description=(
                    "Example of structure and format "
                    "for opening hours field."
                ),
                value={
                    "opening_hours": OPENING_HOURS_SWAGGER_EXAMPLE,
                }
            ),
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
        try:
            serializer = self.get_serializer_class()
            serializer = serializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.create(
                    validated_data=serializer.validated_data,
                    user=request.user
                )
                return Response(status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[ClubActions][create_club] {str(ex)}"
                )
            )
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        tags=["Club"],
        summary="Update existing Club",
        description="PUT request to update existing club",
        # provide Authentication class that deviates from the views default
        operation_id="Update existing club",
        parameters=[
            OpenApiParameter(
                name="Club Name",
                description='Official name of the club',
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club Name: STRING',
                        value='TT Club'
                    ),
                ],
            ),
            OpenApiParameter(
                name="Club State",
                description='State where club is placed',
                required=False,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club State: STRING',
                        value='UAE'
                    ),
                ],
            ),
            OpenApiParameter(
                name="Club City",
                description='City where club is placed',
                required=False,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club City: STRING',
                        value='Abu Dabi'
                    ),
                ],
            ),
            OpenApiParameter(
                name="Club Address",
                description='Street, where club is placed',
                required=False,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club Street: STRING',
                        value='Gagarina st., Houser #7'
                    ),
                ],
            ),
            OpenApiParameter(
                name="Club Phone Number",
                description='Phone number of club',
                required=False,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club Phone Number: STRING',
                        value='89992370953'
                    ),
                ],
            ),
            OpenApiParameter(
                name="Opening Hours",
                description='Days and hours when club is working',
                required=False,
                type=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Club Opening Hours: JSON(DICT)',
                        OPENING_HOURS_SWAGGER_EXAMPLE
                    ),
                ],
            ),
            OpenApiParameter(
                name="About",
                description='Additional info about club',
                required=False,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club About: STRING',
                        "Hello, it's me! I like Pen-Pineapple-Apple-Pen"
                    ),
                ],
            ),
            OpenApiParameter(
                name="Social Link",
                description='Link to club social network page',
                required=False,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club Social Link: STRING',
                        'https://vk.com'
                    ),
                ],
            ),
            OpenApiParameter(
                name="Website Link",
                description='Link to club site, any info in Ethernet',
                required=False,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club Website Link: STRING',
                        "https://welovecocks.com"
                    ),
                ],
            ),
        ],
        responses={
            200: None,
        }
    )
    @action(
        detail=True,
        methods=['put'],
        url_path="update_club",
        parser_classes=(MultiPartParser,)
    )
    def update_club(self, request, id=None) -> Response:
        try:
            instance = self.get_object()
            serializer = self.get_serializer_class()
            serializer = serializer(instance=instance, data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    status=HTTP_200_OK                
                )

            else:

                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[ClubActions][update_club] {str(ex)}"
                )
            )
        
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        tags=["Club"],
        methods=["GET"],
        summary="Get all existing Clubs",
        description="GET request to get all existing clubs by ID",
        operation_id="Get all existing clubs"
    )
    @action(detail=False, methods=['get'], url_path="list_clubs")
    def list_clubs(self, request) -> Response:
        try:
            user = request.user
            queryset = Club.objects.filter(admin_club__user=user).all()
            serializer = self.get_serializer_class()
            serializer = serializer(queryset, many=True)
            serializer = serializer.data

            return Response(status=200, data=serializer)

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[ClubActions][list_clubs] {str(ex)}"
                )
            )
            
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        tags=["Club"],
        methods=["GET"],
        summary="Get existing Club",
        description="GET request to get existing club by ID",
        operation_id="Get existing club by ID",
        responses={
            201: OpenApiResponse(response=ClubGetSerializer,
                                 description='Existing Club Object in response'),
            401: OpenApiResponse(
                response={
                    "detail": "No auth credentials"
                },
                description='No auth credentials.',
                examples=[
                    OpenApiExample(
                        "No auth credentials",
                        value={
                            "detail": "Authentication credentials were not provided."
                        }
                    )
                ]
            ),
        },
    )
    @action(detail=True, methods=['get'], url_path='get_club')
    def get_club(self, request, id=None):
        try:
            club = Club.objects.filter(
                id=id
            ).first()
            serializer = self.get_serializer_class()
            serializer = serializer(club)

            return Response(serializer.data)

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[ClubActions][get_club] {str(ex)}"
                )
            )
            
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST,
            )
        


@extend_schema_view(
    destroy=extend_schema(
        summary='Delete club photo',
        tags=['Club Photo']
    )
)
# NOTE: can use DestroyModelMixin, but it does
# not work with Swagger DRF-spectacular
class ClubPhotosDestroyCreateView(DestroyAPIView, CreateAPIView):
    """ class for deleting club photoes """
    lookup_field = 'id' # only for delete method
    permission_classes = [IsAuthenticated]
    serializer_class = ClubPhotoSerializer
    parser_classes = (MultiPartParser,)
    queryset = ClubPhoto.objects.all()

    def get_queryset(self):
        """ get queryset """        
        if self.request.method == "DELETE":
        
            return ClubPhoto.objects.all()

        return Club.objects.all()

    def destroy(self, request, *args, **kwargs):
        """ delete existing photo"""
        # if request from owner of clubs' photoes
        instance: ClubPhoto = self.get_object()

        # check permission to delete club photo
        if instance.club.admin_club.user == request.user:

            return super().destroy(request, *args, **kwargs)

        else:

            return Response(status=HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        """ add new photo """
        try:

            club = define_club_of_user(user=request.user)

            if club:

                serializer = self.serializer_class
                serializer = serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                ClubPhoto.objects.create(
                    **serializer.validated_data,
                    club=club,
                )
                return Response(status=HTTP_200_OK)
            
            else:

                return Response(status=HTTP_400_BAD_REQUEST)
            
        except Exception as ex:

            asyncio.run(
                telegram_log_errors(
                    f'[ClubPhotosDestroyCreateView][create]{str(ex)}'
                )
            )
            return Response(
                data=str(ex),
                status=HTTP_400_BAD_REQUEST
            )
