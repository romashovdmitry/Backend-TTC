# Django imports
from django.db import models


class TournamentStatus(models.IntegerChoices):

    CREATED = 0, 'CREATED'
    APPROVED = 1, 'APPROVED'
    CONFIGURED = 2, 'CONFIGURED'
    TOURNAMENT_STARTED = 3, 'TOURNAMENT_STARTED'
    RUNING_NOW = 4, 'RUNING_NOW'
    FINISHED = 5, 'FINISHED'


class TournamentType(models.IntegerChoices):
    # it would more in future
    GROUP_KNOCK_OFF = 0, "GROUP_KNOCK_OFF"


DEFAULT_MAX_RATING_LIMIT = 10000
DEFAULT_MIN_RATING_LIMIT = 0
DEFAULT_GROUP_QUALIFIRES_NUMBER = 1


class TournamentStage(models.IntegerChoices):

    START = 0, 'START'
    GROUP_STAGE = 1, 'GROUP_STAGE'


class GameStatus(models.IntegerChoices):

    CREATED = 0, 'CREATED'
    STARTED = 1, 'STARTED'
    FINISHED = 2, 'FINISHED'


GROUP_ALPHABBET = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
    10: "J"
}


# If None that integer instead.
JSON_DICT_PLAYER = {
    "pk": None,
    "grid_id": None,
    "name": ""
}

JSON_DICT_GAMES = {
    "order": None,
    "grid_ids": []
}

JSON_DICT_GROUP = {
    "group_id": None,
    "group_alpha": "",
    "players": [],
    "group_games": None,
    "games": []
}


RCP_MAX_COEFF = 400
Rcp_COEFFICIENTS = [
    {
        "max_value": 100,
        "rcp": 0.2
    },
    {
        "max_value": 200,
        "rcp": 0.25
    },
    {
        "max_value": 300,
        "rcp": 0.3
    },
    {
        "max_value": RCP_MAX_COEFF,
        "rcp":  0.35
    }
]

D_COEFFS = {
    1: 0.8,
    2: 1,
    3: 1.2
}

def return_rcp_coeff(rcp_integer):

    if rcp_integer > RCP_MAX_COEFF:

        return 4

    for rcp_order in range(0, len(Rcp_COEFFICIENTS)):

        if rcp_integer < Rcp_COEFFICIENTS[rcp_order]["max_value"]:

            return Rcp_COEFFICIENTS[rcp_order]["rcp"]
        
STAGE_NAMES = ["1/4", "1/8", "1/16", "1/32", "1/64", "1/128"]
