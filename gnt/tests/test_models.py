"""
Model Tests
"""

# import necessary modules
from django.test import TestCase
from django.contrib.auth.models import User
from gnt.models import Profile

# testing constants
TEST_USERNAME = 'test_username'
TEST_EMAIL = 'test_email'
TEST_PASSWORD = 'test_password'
TEST_IMAGE = 'test_image'
TEST_BIO = 'test_bio'


class UserModelTest(TestCase):
    """
    User Model Test
    """

    def setUp(self):
        """
        User Model Test Set Up
        """

        User.objects.create(username=TEST_USERNAME,
                            email=TEST_EMAIL, password=TEST_PASSWORD)

    def test_retrieve_user(self):
        """
        Test Retrieve User
        """

        user = User.objects.get(username=TEST_USERNAME)
        self.assertTrue(isinstance(user, User))
        self.assertEqual(TEST_USERNAME, user.username)
        self.assertEqual(TEST_EMAIL, user.email)
        self.assertEqual(TEST_PASSWORD, user.password)
