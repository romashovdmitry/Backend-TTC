# import basemodel and django.db.models
from main.base_model import models, BaseModel

# FIXME: не сработала ссылка вида "user.club_admin"
from user.models.club_admin import ClubAdmin


class Club(BaseModel):
    """
    Club model.
    Physical club where
    competitions take place.
    """

    class Meta:
        db_table = "clubs"
        verbose_name = "Club"
        verbose_name_plural = "Clubs"

    name = models.CharField(
        max_length=128,
        null=True,
        verbose_name="Club Name",
        help_text="Official name of club"
    )

    logo = models.BinaryField(
        null=True,
        verbose_name="Club Logo",
        help_text="Club logo"
    )

    club_photoes = models.JSONField(
        null=True
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

    # NOTE: in future maybe we can use
    # package https://github.com/daviddrysdale/python-phonenumbers
    # but now i don't see strong reason for that
    phone_number = models.CharField(
        null=True,
        verbose_name="Phone number",
        help_text="Phone number of club"
    )

    opening_hours = models.JSONField(
        null=True,
        verbose_name="Opening hours",
        help_text="Days and hours when club is working"
    )

    about = models.TextField(
        null=True,
        verbose_name="About Club",
        help_text="Additional info about club"        
    )

    social_link = models.URLField(
        null=True,
        verbose_name="Club Social Network page",
        help_text="Link to club social network page"
    )

    link = models.URLField(
        null=True,
        verbose_name="Club Site",
        help_text="Link to club site, any info in Ethernet"
    )

    admin_club = models.ForeignKey(
        ClubAdmin,
        null=True,
        on_delete=models.SET_NULL,
        related_name="admin_club"
    )