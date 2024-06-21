# DRF imports
from rest_framework.permissions import IsAuthenticated

# import models
from club.models.club import Club
from user.models.club_admin import ClubAdmin


class IsClubAdmin(IsAuthenticated):
    message = "Only club owners can perform this action."

    def has_permission(self, request, view):
        # Проверяем, является ли текущий пользователь владельцем клуба
        user = request.user
        club_id = request.data.get('club')
        club = Club.objects.filter(pk=club_id).first()
        return request.club_admin == club.admin_club
