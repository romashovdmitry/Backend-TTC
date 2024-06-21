# Django imports
from django.utils.deprecation import MiddlewareMixin

# import models
from user.models.player import Player
from user.models.club_admin import ClubAdmin


class UserDataMiddleware(MiddlewareMixin):
    """ to optimize request object """
    def process_request(self, request):
        """ 
        1. add to request object 
            field user_id, which equal to request.user.id
        2. add to request object 
            field player which get Player object for user
            or None
        3. add to request object
            field ClubAdmin which get ClubAdmin object for user
            or None        
        """
        if request.user.is_authenticated:
            request.user_id = request.user.id
            request.club_admin = ClubAdmin.objects.filter(user=request.user).first()
            request.player = Player.objects.filter(user=request.user).first()
        else:
            request.user_id = None