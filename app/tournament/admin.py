# Django imports
from django.contrib import admin

# import models
from tournament.models import Tournament, TournamentPlayers


class TournamentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "date_time",
        "min_rating_limit",
        "max_rating_limit",
        "club",
        "tournament_admin"
    ]

class TournamentPlayersAdmin(admin.ModelAdmin):
    pass

admin.site.register(TournamentPlayers, TournamentPlayersAdmin)
admin.site.register(Tournament, TournamentAdmin)
