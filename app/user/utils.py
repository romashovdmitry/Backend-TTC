# Python imports
import random
from datetime import date


async def create_random_code(random_code: str = "") -> str:
    """
    Create random code for first Tournament Admin
    or Club Admin visit to web-club.

    Return:
        str: 6-length string with random digits
    """
    for _ in range(6):
        random_code += str(random.randint(0, 9))
    return random_code


create_date_for_json_to_frontend = lambda date_from_database: (
    f"{date_from_database.day}."
    f"{date_from_database.month}."
    f"{date_from_database.year}"
)