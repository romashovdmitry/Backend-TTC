# Django imports
from django.contrib import admin

# import models
from club.models.club import Club


class ClubAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "state",
        "city",
        "address",
        "about",
        "link"
    ]


admin.site.register(Club, ClubAdmin)
