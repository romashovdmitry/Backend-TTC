# Python imports
import random


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
