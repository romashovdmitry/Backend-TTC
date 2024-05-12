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


class ClubActions(ViewSet, RetrieveAPIView):
    """ class for creating and updating clubs """
    parser_classes = (MultiPartParser,)
    http_method_names = ['post', 'put', 'get']
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    queryset = Club.objects.all()

    def get_serializer_class(self):
        """ define serializer for class """

        if self.action == 'create_club' or self.action == 'update_club':
            return ClubCreateUpdateSerializer

        elif self.action == "list_clubs":
            return ShowAllClubsSerializer

        elif self.action == "get_club":
            return ClubGetSerializer

    @extend_schema(
        tags=["Club"],
        summary="Create new Club",
        description="POST request to create new club",
        operation_id="Create new club",
        parameters=[
            OpenApiParameter(
                name="Club Name",
                description='Official name of the club',
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        'Club Name: STRING',
#                        summary='Email exampls',
                        value='TT Club'
                    ),
                ],
            ),
# NOTE: закомментировано специально
#            OpenApiParameter(
#                name="logo",
#                description='Club logo',
#                required=True,
#                type=OpenApiTypes.BINARY,
#            ),
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
        # NOTE: можно добавить responses, если будет время
        # пример для 401 ответ уже есть в этом файле
        responses={
            200: None,
        }
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
            instance = serializer.create(
                validated_data=serializer.validated_data,
                user=request.user
            )
            instance.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

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

    @extend_schema(
        tags=["Club"],
        methods=["GET"],
        summary="Get all existing Clubs",
        description="GET request to get all existing clubs by ID",
        operation_id="Get all existing clubs"
    )
    @action(detail=False, methods=['get'], url_path="list_clubs")
    def list_clubs(self, request) -> Response:
        user = request.user
        queryset = Club.objects.filter(admin_club__user=user).all()
        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True)
        serializer = serializer.data

        return Response(status=200, data=serializer)

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
    def get_club(self, request, pk=None):
        club = Club.objects.filter(
            id=pk
        ).first()
        serializer = self.get_serializer_class()
        serializer = serializer(club)
        return Response(serializer.data)
