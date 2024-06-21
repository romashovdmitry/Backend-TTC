# Django imports
from django.db import models


class TournamentStatus(models.IntegerChoices):

    CREATED = 0, 'CREATED'
    APPROVED = 1, 'APPROVED'
    STARTED = 2, 'STARTED'
    RUNING_NOW = 3, 'RUNING_NOW'
    FINISHED = 4, 'FINISHED'


class TournamentType(models.IntegerChoices):
    # it would more in future
    GROUP_KNOCK_OFF = 0, "GROUP_KNOCK_OFF"