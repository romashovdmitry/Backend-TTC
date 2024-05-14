""" small helper-functions that could be used in several or all apps """
# Python imports
import logging
from PIL import Image

# Django imports
from django.db.models import Model  # because of circular imports
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


# FIXME: лучше аннотирование сделать
def define_image_file_path(
        filename: str,
        directory: str,
        object_type: str,
        instance_indicator: str
):
    """
    Define path for uploaded to API image.

    Parameters:
        filename: string with name of file
        directory: path where photoes are saved
            inside media directory
        instance: object of model Player, Club
            or another
    Returns:
        str: filename that would be used for
            saving file in project
            
    """
    try:
        return directory + instance_indicator + object_type + filename.split(".")[-1]

    except Exception as ex:
        # FIXME: здесь логгирование должно быть
        logger.error(
            f'main.utils.define_image_file_path: {ex}'
        )

        return filename


# NOTE: добавить аннотирование типа данных
# расширить (Parameters, Returns) аннотацию ф-ции
def image_file_extension_validator(object):
    """
    Check file-extension for case when format
    in filename not equal to real format. 
    For example, example.jpc could be filename,
    but jpg is real file-extension.
    """
    try:

        image_format = Image.open(object).format
        filename = str(object)
        filename_file_extension = filename.split(".")[-1]

        if not (image_format.lower() in ["jpeg", "jpg"] and filename_file_extension.lower() in ["jpeg", "jpg"]):

            if image_format.lower() != filename_file_extension.lower():

                raise ValidationError(
                    "Real file-extension is not equal to "
                    "file-extension in filename. "
                    "Please, redefine filename by the correct way. "
                    f"Filename: {str(object)}"
                )

        return object

    except Exception as ex:
        # FIXME: здесь логгирование должно быть
        print(ex)
        raise ValidationError(
            "Real file-extension is not equal to "
            "file-extension in filename. "
            "Please, redefine filename by the correct way."
            f"Filename: {str(object)}"
        )