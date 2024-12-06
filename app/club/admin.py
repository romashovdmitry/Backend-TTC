# Django imports
from django.contrib import admin
from django.utils.html import format_html

# import models
from club.models import (
    Club,
    ClubPhoto
)
from user.models import (
    ClubAdmin as ClubAdmin_Model
)


class ClubPhotoAdmin(admin.ModelAdmin):
    """ Admin settongs for ClubPhoto objects """
    list_display = ["club", "photo_image"]

    # https://dev.to/vijaysoni007/how-to-show-images-of-the-model-in-django-admin-5hk4
    def photo_image(self, obj: ClubPhoto):
        """ to show logo-image in admin panel for club """
        if obj.photo:
            return format_html('<img src="{}" style="max-width:200px; max-height:100px"/>'.format(obj.photo.url))

        else:
            return "-"


class ClubAdmin(admin.ModelAdmin):
    """ Admin settings for Club objects """
    list_display = [
        "pk",
        "name",
        "state",
        "city",
        "address",
        "about",
        "link",
        "logo_image"
    ]

    # https://dev.to/vijaysoni007/how-to-show-images-of-the-model-in-django-admin-5hk4
    def logo_image(self, obj: Club):
        """ to show logo-image in admin panel for club """
        if obj.logo:
            return format_html('<img src="{}" style="max-width:200px; max-height:100px"/>'.format(obj.logo.url))

        else:
            return "-"

# FIXME: сменить название класса
class ClubAdminAdmin(admin.ModelAdmin):
    pass


admin.site.register(ClubAdmin_Model, ClubAdminAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(ClubPhoto, ClubPhotoAdmin)
