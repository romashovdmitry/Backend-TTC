# DRF imports
from rest_framework.permissions import IsAuthenticated

# import models
from club.models import Club
from tournament.models import Tournament

class IsClubAdmin(IsAuthenticated):
    message = "Only club owners can perform this action."

    def has_permission(self, request, view):

        try:
            # Проверяем, является ли текущий пользователь владельцем клуба
            club_pk = request.data.get('club')
            tournament_pk = request.data.get('tournament')

            if not club_pk:
                club_pk = view.kwargs.get('club_pk')

                if not club_pk:

                    if tournament_pk:
                        club_pk = Tournament.objects.filter(
                            pk=tournament_pk
                        ).first().club.pk
                        
                    else:
                        
                        return False

            # NOTE: we think that club only one for admin
            # on start of project 
            club = Club.objects.filter(pk=club_pk).first()
            
            return request.club_admin == club.admin_club if club else False

        # leave it like this
        except:

            return False