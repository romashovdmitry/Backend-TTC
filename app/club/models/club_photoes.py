# Python imports
import os

# import basemodel and django.db.models
from typing import Iterable
from main.base_model import BaseModel, models

# import custom foos, classes
from main.utils import image_file_extension_validator

from main.settings import MEDIA_ROOT

# FIXME: улучшить аннотирование
def define_club_photo_path(instance, filename):
    """
    define club logo path
    """
    try:
        return "club_photoes/" + filename.replace(" ", "_")

    except Exception as ex:
        # FIXME: здесь логгирование должно быть
        print(ex)
        return filename


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

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        # change name of file
        # we can't do that before, because
        # need to know club name and model object
        # isn't created before this step
        try:
            club_photo_directory = 'club_photoes/'
            club_name = (
                "club_pk_" +
                str(self.club.pk) +
                "_photo_pk_" +
                str(self.pk) +
                "." +
                (str(self.photo).split(".")[-1]).replace(" ", "_")
            )

            os.rename(
                MEDIA_ROOT + "/" + str(self.photo),
                MEDIA_ROOT + "/" + club_photo_directory + club_name
            )
            self.photo = club_photo_directory + club_name
        except Exception as ex:
            # FIXME: здесь логгирование должно быть
            print(ex)

        finally:
            return super().save()
        