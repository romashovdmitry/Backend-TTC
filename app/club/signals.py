# Python imports
import os
import asyncio

# Django imports
from django.db.models.signals import pre_save
from django.dispatch import receiver
from main.base_model import BaseModel

# import models
from .models import Club

# import config data, constants
from main.settings import MEDIA_ROOT


# FIXME: это можно убрать и убрать ещё из app.pe код сигналов
@receiver(pre_save, sender=Club)
async def delete_old_logo(sender: BaseModel, instance: Club, **kwargs):
    """
    пока тут ничего. см. ниже, что было. перенёс в переопределение метода
    save для модели Club
    """
    pass



"""
    new_image = Image.open(instance.logo)
    pk = instance.pk
    obj = await Club.objects.aget(pk=pk)
    current_image_path = MEDIA_ROOT + '/' + str(obj.logo)
    current_image = Image.open(current_image_path)
    # https://stackoverflow.com/a/56280735/24040439
    try:
        diff = ImageChops.difference(new_image, current_image)

        if diff.getbbox():
            os.remove(current_image_path)

    except Exception as ex:
        os.remove(current_image_path)
"""