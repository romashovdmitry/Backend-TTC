# Django imports
from django.utils.deprecation import MiddlewareMixin

# JWT imports
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

# import models
from user.models.player import Player
from user.models.club_admin import ClubAdmin


# https://docs.djangoproject.com/en/5.0/topics/http/middleware/#writing-your-own-middleware
class UserDataMiddleware(MiddlewareMixin):
    """ to optimize request object """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """ add user_id key-valuepair to requst.data from request.user.id """
        authorization_header = request.headers.get('Authorization')
        request.club_admin = None

        if authorization_header:

            try:
                token_type, token = authorization_header.split()

                if token_type.lower() == 'bearer':
                    jwt_authentication = JWTTokenUserAuthentication()
                    user, validated_token = jwt_authentication.authenticate(request)

                    if user:
                        request.user_id = user.id
                        request.club_admin = ClubAdmin.objects.filter(
                            user=request.user_id
                        ).first()
                        request.player = Player.objects.filter(
                            user=request.user_id
                        ).first()
            except:
                # wrong header format

                return self.get_response(request)

        response = self.get_response(request)

        return response
