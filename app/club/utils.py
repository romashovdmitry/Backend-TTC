# python imports
from datetime import date, datetime

# import models
from user.models.user import User
from club.models.club import Club

# import constants
from club.constants import MONTHES


def define_club_of_user(
        user_object: User,
) -> Club | None:
    """
    Define Club for user. It could be used
    in update Club, get, delete Club views.

    Parameters:
        user_object: User object got from request (request.user)
    Returns:
        Club | None: django model object of Club models
            or None, if not exists Club.
    """
    return Club.objects.filter(admin_club__user=user_object).first()


def create_tournament_date_for_json_to_frontend(date_time: datetime):
    """
    make date from datetime for club get query
    """

    return f'{date_time.day} {MONTHES[date_time.month]}'


def create_tournament_time_for_json_to_frontend(date_time: datetime):
    """
    make time from datetime for club get query
    """

    return f'{date_time.hour}:{date_time.minute}'
