# Django imports
from typing import Any
from django.db import models


class BaseModel(models.Model):
    """ Base class for inheritance by others except model User """

    class Meta:
        ordering = ['-created']
        abstract = True

    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name="Created date, time",
        help_text="Created date, time",
        null=True
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Created date, time",
        help_text="Update date, time",
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Object is active of not",
        help_text=(
            "Project use this field "
            "instead of full removing "
            "object from database. Just "
            "deactivate "
        ),
    )

    def delete(self):
        self.is_active = False
        self.save()

        return self
