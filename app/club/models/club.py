# Python imports
import re
import os
from PIL import Image
from django.core.exceptions import ValidationError
import hashlib

# import basemodel and django.db.models
from main.base_model import models, BaseModel
# FIXME: не сработала ссылка вида "user.club_admin"
from user.models.club_admin import ClubAdmin

# import constants
from club.constants import CLUB_FEATURES_HELP_TEXT, OPENING_HOURS_SWAGGER_EXAMPLE_2

# import custom foos, classes
from main.utils import image_file_extension_validator

# import constants, config data
from main.settings import MEDIA_ROOT

# import custom foos, classes
from main.utils import (
    define_image_file_path,
    get_image_hash
)


# FIXME: улучшить аннотирование
def define_logo_path(instance, filename):
    """
    define club logo path
    """
    return define_image_file_path(
        instance_indicator=instance.name,
        filename=filename,
        object_type="_logo.",
        directory="logos/"
    )


class Club(BaseModel):
    """
    Club model.
    Physical club where
    competitions take place.
    """

    class Meta:
        db_table = "clubs"
        verbose_name = "Club"
        verbose_name_plural = "Clubs"

    name = models.CharField(
        unique=True,
        max_length=128,
        null=True,
        verbose_name="Club Name",
        help_text="Official name of club",
        error_messages={'unique': "This club name already exists. Please choose another name."},  
    )

    logo = models.ImageField(
        upload_to=define_logo_path,
        null=True,
        verbose_name="Club Logo",
        help_text="Club logo",
        validators=[image_file_extension_validator]
    )

    # NOTE: можно ограничить, скачав необходимую библиотеку
    state = models.CharField(
        max_length=64,
        null=True,
        verbose_name="State",
        help_text="State where club is placed"
    )

    city = models.CharField(
        max_length=64,
        null=True,
        verbose_name="City",
        help_text="City where club is placed"
    )

    address = models.CharField(
        max_length=256,
        null=True,
        verbose_name="Club Address",
        help_text="Street, where club is placed"
    )

    # NOTE: in future maybe we can use
    # package https://github.com/daviddrysdale/python-phonenumbers
    # but now i don't see strong reason for that
    phone_number = models.CharField(
        max_length=32,
        null=True,
        verbose_name="Phone number",
        help_text="Phone number of club"
    )

    opening_hours = models.JSONField(
        null=True,
        verbose_name="Opening hours",
        help_text=OPENING_HOURS_SWAGGER_EXAMPLE_2
    )

    about = models.TextField(
        null=True,
        verbose_name="About Club",
        help_text="Additional info about club"        
    )

    social_link = models.URLField(
        null=True,
        verbose_name="Club Social Network page",
        help_text="Link to club social network page"
    )

    link = models.URLField(
        null=True,
        verbose_name="Club Site",
        help_text="Link to club site, any info in Ethernet"
    )

    features = models.JSONField(
        null=True,
        verbose_name="Club Features",
        help_text=(
            'Данное поле следует заполнять '
            'строго в таком порядке: '
            f'{CLUB_FEATURES_HELP_TEXT}'
        )
    )

    admin_club = models.ForeignKey(
        ClubAdmin,
        null=True,
        on_delete=models.SET_NULL,
        related_name="admin_club"
    )

    def save(self, *args, **kwargs):
        """
        redefine method for removing image,
        if it's updating.
        """
        # FIXME: тут было удалениие файла фото,
        # которое больше не используется.
        super(Club, self).save(*args, **kwargs)

    def __str__(self):

        return self.name
