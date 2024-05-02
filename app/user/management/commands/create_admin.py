# Django import
from django.core.management.base import BaseCommand

# import models
from user.models.user import User

# .env libs import
import os
from dotenv import load_dotenv
load_dotenv()


class Command(BaseCommand):
    """ autocreate admin user """
    def handle(self, *args, **options):
        email = os.getenv('SUPER_EMAIL')

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email)
            self.stdout.write("Superuser created!")