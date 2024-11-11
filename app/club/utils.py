# import models
from user.models.user import User
from club.models.club import Club


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
