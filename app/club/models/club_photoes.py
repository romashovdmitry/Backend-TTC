# Python imports
import os
import asyncio

# import basemodel and django.db.models
from typing import Iterable
from main.base_model import BaseModel, models

# import custom foos, classes
from main.utils import image_file_extension_validator

# import constants, config data
from main.settings import MEDIA_ROOT

# import custom foos, classes
from main.utils import define_image_file_path
from telegram_bot.send_error import telegram_log_errors

# FIXME: улучшить аннотирование
def define_club_photo_path(instance, filename):
    """
    define club logo path
    """
    return define_image_file_path(
        instance_indicator=instance.club.name,
        filename=filename,
        object_type="_club_photo.",
        directory="club_photoes/"
    )


class ClubPhoto(BaseModel):
    """
    Model for storage photoes URLs
    """
    class Meta:
        db_table = "club_photoes"
        verbose_name = "Club Photo"
        verbose_name_plural = "Club Photoes"

    # don't need this field in this model
    is_active = None

    photo = models.ImageField(
        upload_to=define_club_photo_path,
        null=True,
        verbose_name="Url of club Photo",
        help_text=(
            "URL on which project store "
            "photo's URL on server"
        ),
        validators=[image_file_extension_validator]
    )
    club = models.ForeignKey(
        "club.club",
        on_delete=models.CASCADE
    )

    def delete(self) -> tuple[int, dict[str, int]]:
        try:
            os.remove(MEDIA_ROOT + "/" + str(self.photo))

        except Exception as ex:
            asyncio.run(
                telegram_log_errors(
                    f"[ClubPhoto Model][delete] {str(ex)}"
                )
            )

        return super(ClubPhoto, self).delete()
