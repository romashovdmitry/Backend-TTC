# Django imports
from django.contrib import admin

# import models
from user.models.user import User
from user.models.player import Player
from user.models.tournament_admin import TournamentAdmin


# NOTE: not done
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user']
#    search_fields = ['email']

    @admin.display()
    def view_user_email(self, obj):
        return obj.user.email


class UserAdmin(admin.ModelAdmin):
    list_display = ['email']
    search_fields = ['email']


class TournamentAdmin__Admin(admin.ModelAdmin):
    list_display = ['user']

    @admin.display()
    def view_user_email(self, obj):
        return obj.user.email

admin.site.register(User, UserAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(TournamentAdmin, TournamentAdmin__Admin)
