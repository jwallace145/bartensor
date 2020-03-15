"""
Model Tests
"""

# import necessary modules
from django.test import TestCase
import datetime
import pytz
from unittest import mock
from django.contrib.auth.models import User
from gnt.models import Friend, FriendRequest, Profile, UserDrink


class UserModelTest(TestCase):
    """
    User Model Test
    """

    # constants
    TEST_USERNAME = 'test_username'
    TEST_EMAIL = 'test_email'
    TEST_PASSWORD = 'test_password'

    def test_create_and_save_user(self):
        """
        Test Create and Save User
        """

        user = User.objects.create(username=self.TEST_USERNAME,
                                   email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

        self.assertTrue(isinstance(user, User))
        self.assertEqual(self.TEST_USERNAME, user.username)
        self.assertEqual(self.TEST_EMAIL, user.email)
        self.assertEqual(self.TEST_PASSWORD, user.password)


class ProfileModelTest(TestCase):
    """
    Profile Model Test
    """

    # constants
    TEST_USERNAME = 'test_username'
    TEST_EMAIL = 'test_email'
    TEST_PASSWORD = 'test_password'
    TEST_IMAGE = 'default.jpg'
    TEST_BIO = 'test_bio'

    def test_create_and_save_profile(self):
        """
        Test Create and Save Profile
        """

        user = User.objects.create(
            username=self.TEST_USERNAME, email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

        profile = Profile.objects.get(user=user)
        profile.image = self.TEST_IMAGE
        profile.bio = self.TEST_BIO
        profile.save()

        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(user, profile.user)
        self.assertEqual(self.TEST_IMAGE, profile.image)
        self.assertEqual(self.TEST_BIO, profile.bio)


class FriendRequestModelTest(TestCase):
    """
    Friend Request Model Test
    """

    # constants
    TEST_USERNAME1 = 'test_username1'
    TEST_EMAIL1 = 'test_email1'
    TEST_PASSWORD1 = 'test_password1'
    TEST_BIO1 = 'test_bio1'
    TEST_IMAGE1 = 'default.jpg'
    TEST_USERNAME2 = 'test_username2'
    TEST_EMAIL2 = 'test_email2'
    TEST_PASSWORD2 = 'test_password2'
    TEST_BIO2 = 'test_bio2'
    TEST_IMAGE2 = 'default.jpg'

    def test_create_and_save_friend_request(self):
        """
        Test Create and Save Friend Request
        """

        user_requestee = User.objects.create(
            username=self.TEST_USERNAME1, email=self.TEST_EMAIL1, password=self.TEST_PASSWORD1)
        user_requestor = User.objects.create(
            username=self.TEST_USERNAME2, email=self.TEST_EMAIL2, password=self.TEST_PASSWORD2)

        requestee = Profile.objects.get(user=user_requestee)
        requestee.bio = self.TEST_BIO1
        requestee.image = self.TEST_IMAGE1
        requestee.save()

        requestor = Profile.objects.get(user=user_requestor)
        requestor.bio = self.TEST_BIO2
        requestor.image = self.TEST_IMAGE2
        requestor.save()

        friend_request = FriendRequest.objects.create(
            requestee=requestee, requestor=requestor)

        self.assertTrue(isinstance(friend_request, FriendRequest))
        self.assertEquals(user_requestee, friend_request.requestee.user)
        self.assertEquals(user_requestor, friend_request.requestor.user)
        self.assertEquals(requestee, friend_request.requestee)
        self.assertEquals(requestor, friend_request.requestor)


class FriendModelTest(TestCase):
    """
    Friend Model Test
    """

    # constants
    TEST_USERNAME1 = 'test_username1'
    TEST_EMAIL1 = 'test_email1'
    TEST_PASSWORD1 = 'test_password1'
    TEST_BIO1 = 'test_bio1'
    TEST_IMAGE1 = 'default.jpg'
    TEST_USERNAME2 = 'test_username2'
    TEST_EMAIL2 = 'test_email2'
    TEST_PASSWORD2 = 'test_password2'
    TEST_BIO2 = 'test_bio2'
    TEST_IMAGE2 = 'default.jpg'

    def test_create_and_save_friends(self):
        """
        Test Create and Save Friends
        """

        user_friend1 = User.objects.create(
            username=self.TEST_USERNAME1, email=self.TEST_EMAIL1, password=self.TEST_PASSWORD1)
        user_friend2 = User.objects.create(
            username=self.TEST_USERNAME2, email=self.TEST_EMAIL2, password=self.TEST_PASSWORD2)

        friend1 = Profile.objects.get(user=user_friend1)
        friend1.bio = self.TEST_BIO1
        friend1.image = self.TEST_IMAGE1
        friend1.save()

        friend2 = Profile.objects.get(user=user_friend2)
        friend2.bio = self.TEST_BIO2
        friend2.image = self.TEST_IMAGE2
        friend2.save()

        friends = Friend.objects.create(friend1=friend1, friend2=friend2)

        self.assertTrue(isinstance(friends, Friend))
        self.assertEquals(user_friend1, friends.friend1.user)
        self.assertEquals(user_friend2, friends.friend2.user)
        self.assertEquals(friend1, friends.friend1)
        self.assertEquals(friend2, friends.friend2)


class UserDrinkModelTest(TestCase):
    """
    User Drink Model Test
    """

    # constants
    TEST_USERNAME = 'test_username'
    TEST_EMAIL = 'test_email'
    TEST_PASSWORD = 'test_password'
    TEST_NAME = 'test_name'
    TEST_DESCRIPTION = 'test_description'
    TEST_TIMESTAMP = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    TEST_LIKES = 0
    TEST_IMAGE = 'default.jpg'

    def test_create_and_save_user_drink(self):
        mocked = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            user = User.objects.create(
                username=self.TEST_USERNAME, email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

            drink = UserDrink.objects.create(
                user=user, name=self.TEST_NAME, description=self.TEST_DESCRIPTION, likes=self.TEST_LIKES, image=self.TEST_IMAGE)

            self.assertTrue(isinstance(drink, UserDrink))
            self.assertEquals(user, drink.user)
            self.assertEquals(self.TEST_NAME, drink.name)
            self.assertEquals(self.TEST_DESCRIPTION, drink.description)
            self.assertEquals(self.TEST_TIMESTAMP, drink.timestamp)
            self.assertEquals(self.TEST_LIKES, drink.likes)
            self.assertEquals(self.TEST_IMAGE, drink.image)
