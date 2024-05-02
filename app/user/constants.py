"""
constant data for user app foos, models, services
"""

# error messages
PASSWORD_IS_REQUIRED = "Password is required for new user"
EMAIL_IS_REQUIRED = "User must have any email for registrations"

# for Player models
MALE = 0
FEMALE = 1

GENDER_CHOISE = (
    (MALE, "MALE"),
    (FEMALE, "FEMALE")
)

RIGHT_HAND = 0
LEFT_HAND = 1
BOTH = 2

HAND_CHOISE = (
    (RIGHT_HAND, "RIGHT_HAND"),
    (LEFT_HAND, "LEFT_HAND"),
    (BOTH, "BOTH")
)