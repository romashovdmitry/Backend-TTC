# Django imports
from django.contrib import admin

# import models
from user.models.user import User
from user.models.player import Player
from user.models.tournament_admin import TournamentAdmin


# NOTE: not done
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating']

    @admin.display()
    def view_user_email(self, obj):
        return obj.user.email


class UserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email', 'get_rating']
    search_fields = ['__str__', 'email', 'get_rating']


class TournamentAdmin__Admin(admin.ModelAdmin):
    list_display = ['user']

    @admin.display()
    def view_user_email(self, obj):
        return obj.user.email

admin.site.register(User, UserAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(TournamentAdmin, TournamentAdmin__Admin)
