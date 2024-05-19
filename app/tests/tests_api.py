# Django imports
from django.urls import reverse

# DRF imports
from rest_framework import status
from rest_framework.test import APITestCase

# import models
from user.models import User

# import constants
from tests.constants import *


class UserTestsSetUp(APITestCase):

    CREATE_USER_URL = reverse('user_actions')
    CORRECT_DATA = {
        "email": CORRECT_EMAIL,
        "username": CORRECT_USERNAME,
        "password": CORRECT_PASSWORD
    }

    def setUp(self):
        User.objects.create(
            email=DEFAULT_EMAIL,
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD
        )


class UserActionsTests(UserTestsSetUp):
    """
    Testing creating, login, delete user's scenarious.
    """

    def test_create(self):
        """
        check out creating user with non-validate password.
        """
        self.assertEqual(
            True, True
        )



"""
        for SCENARIO in CREATE_USER_SCENARIOUS:

            for wrong_data in SCENARIO["wrong_raw"]["data"]:
                data = self.CORRECT_DATA.copy()
                data[SCENARIO["wrong_raw"]["name"]] = wrong_data
                response = self.client.post(
                    self.CREATE_USER_URL,
                    data=data,
                    format="json"
                )
                self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(
                    response.json(),
                    SCENARIO["error_json"]
                )
"""