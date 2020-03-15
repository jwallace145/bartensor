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
TEST_IMAGE = 'default.jpg'
TEST_BIO = 'test_bio'


class UserModelTest(TestCase):
    """
    User Model Test
    """

    def test_create_and_save_user(self):
        """
        Test Create and Save User
        """
        User.objects.create(username=TEST_USERNAME,
                            email=TEST_EMAIL, password=TEST_PASSWORD)

        user = User.objects.get(username=TEST_USERNAME)

        self.assertTrue(isinstance(user, User))
        self.assertEqual(TEST_USERNAME, user.username)
        self.assertEqual(TEST_EMAIL, user.email)
        self.assertEqual(TEST_PASSWORD, user.password)


class ProfileModelTest(TestCase):
    """
    Profile Model Test
    """

    def test_create_and_save_profile(self):
        user = User.objects.create(username=TEST_USERNAME,
                                   email=TEST_EMAIL, password=TEST_PASSWORD)

        profile = Profile.objects.get(user=user)
        profile.image = TEST_IMAGE
        profile.bio = TEST_BIO
        profile.save()

        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(user, profile.user)
        self.assertEqual(TEST_IMAGE, profile.image)
        self.assertEqual(TEST_BIO, profile.bio)
