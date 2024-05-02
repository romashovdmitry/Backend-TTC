# Django imports
from django.contrib import admin

# import models
from user.models.user import User
from user.models.player import Player
from user.models.club_admin import ClubAdmin


# NOTE: not done
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user']
#    search_fields = ['email']

    @admin.display()
    def view_user_email(self, obj):
        return obj.user.email

admin.site.register(Player, PlayerAdmin)
