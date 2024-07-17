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
