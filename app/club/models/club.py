# Django imports
from django.db import models


class Club(models.Model):
    """
    Club model.
    Physical club where
    competitions take place.
    """
    name = models.CharField(
        max_length=128,
        null=True,
        verbose_name="Club Name",
        help_text="Official name of club"
    )
    state = models.CharField(
        max_length=64,
        null=True,
        verbose_name="State",
        help_text="State where club is placed"
    )

    city = models.CharField(
        max_length=64,
        null=True,
        verbose_name="City",
        help_text="City where club is placed"
    )

    address = models.CharField(
        max_length=256,
        null=True,
        verbose_name="Club Address",
        help_text="Street, where club is placed"
    )

    about = models.TextField(
        null=True,
        verbose_name="About Club",
        help_text="Additional info about club"        
    )

    link = models.URLField(
        null=True,
        verbose_name="Club Site",
        help_text="Link to club site, any info in Ethernet"
    )
