# Django imports
from django.contrib import admin

# import models
from tournament.models.tournament import Tournament


class TournamentAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "date_time",
        "max_players_amount",
        "min_rating_limit",
        "max_rating_limit",
        "club",
        "tournament_admin"
    ]


admin.site.register(Tournament, TournamentAdmin)
