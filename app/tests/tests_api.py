from django.test import TestCase

# Create your tests here.
# Python imports
from unittest import mock

# Django imports
from django.urls import reverse

# DRF imports
from rest_framework import status
# https://stackoverflow.com/a/21012054: pytest without DB
from django.test import SimpleTestCase

# import constants
from tests.constants import *


class UserTestsSetUp(SimpleTestCase):

    MAKE_REQUEST = reverse('create_google_doc')
    CORRECT_DATA = {
        "name": "textname.txt",
        "data": "short string with text about love to Python"
    }


class MakeRequestToApi(UserTestsSetUp):
    """
    Testing request's scenarious.
    """
#    @mock.patch("google_drive_api.constants.FILE_SIZE_LIMIT", new=0)
    def test_request(self):
        """
        Check out request with wrong data.
        """
        for SCENARIO in MAKE_REQUEST_SCENARIOS:

            for wrong_data in SCENARIO["wrong_raw"]["data"]:

                data = self.CORRECT_DATA.copy()
                data[SCENARIO["wrong_raw"]["name"]] = wrong_data
                response = self.client.post(
                    self.MAKE_REQUEST,
                    data=data,
                    content_type="application/json"
                )
                self.assertNotEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(
                    response.json(),
                    SCENARIO["error_json"]
                )

