# Django imports
from django.contrib import admin
from django.utils.html import format_html

# import models
from club.models.club import Club


class ClubAdmin(admin.ModelAdmin):
    """ Admin settings for Club objects """
    list_display = [
        "name",
        "state",
        "city",
        "address",
        "about",
        "link",
        "logo_image"
    ]

    # https://dev.to/vijaysoni007/how-to-show-images-of-the-model-in-django-admin-5hk4
    def logo_image(self, obj):
        """ to show logo-image in admin panel for club """
        if obj.logo:
            return format_html('<img src="{}" style="max-width:200px; max-height:100px"/>'.format(obj.logo.url))

        else:
            return "-"


admin.site.register(Club, ClubAdmin)
