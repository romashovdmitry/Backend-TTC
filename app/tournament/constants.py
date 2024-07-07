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