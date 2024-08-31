# DRF imports
from rest_framework.permissions import IsAuthenticated

# import models
from club.models import Club
from tournament.models import (
    Tournament,
    Game
)


class IsClubAdmin(IsAuthenticated):
    message = "Only club owners can perform this action."

    def has_permission(self, request, view):

        try:
            # NOTE FIXME: это можно улучшить. довольно ублюдски написано
            club_pk = request.data.get('club')
            tournament_pk = request.data.get('tournament')
            game_pk = request.data.get("game_pk")

            if not club_pk:
                club_pk = view.kwargs.get('club_pk')

                if not club_pk:

                    if tournament_pk:
                        club_pk = Tournament.objects.filter(
                            pk=tournament_pk
                        ).first().club.pk

                    elif view.kwargs.get('tournament_pk'):
                        club_pk = Tournament.objects.filter(
                            pk=view.kwargs.get('tournament_pk')
                        ).first().club.pk

                    elif game_pk:
                        club_pk = Game.objects.filter(
                            pk=game_pk
                        ).first().tournament.club.pk

                    elif view.kwargs.get("game_pk"):
                        club_pk = Game.objects.filter(
                            pk=view.kwargs.get("game_pk")
                        ).first().tournament.club.pk

                    else:
                        
                        return False

            # NOTE: we think that club only one for admin
            # on start of project 
            club = Club.objects.filter(pk=club_pk).first()
            
            return request.club_admin == club.admin_club if club else False

        # leave it like this
        except:

            return False