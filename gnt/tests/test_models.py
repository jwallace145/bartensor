"""
Model Tests
"""

# import necessary modules
import datetime
import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from unittest import mock
from gnt.models import Friend
from gnt.models import FriendRequest
from gnt.models import Drink
from gnt.models import DrinkName
from gnt.models import Ingredient
from gnt.models import Instruction
from gnt.models import LikeUserDrink
from gnt.models import Profile
from gnt.models import ProfileToDislikedDrink
from gnt.models import ProfileToLikedDrink
from gnt.models import UserDrink
from gnt.tests import constants


class UserModelTest(TestCase):
    """
    User Model Test
    """

    def test_create_and_save_user(self):
        """
        Create User Model Test
        """

        user = User.objects.create(
            username=constants.TEST_USERNAME,
            email=constants.TEST_EMAIL,
            password=constants.TEST_PASSWORD
        )

        self.assertTrue(isinstance(user, User))
        self.assertEqual(constants.TEST_USERNAME, user.username)
        self.assertEqual(constants.TEST_EMAIL, user.email)
        self.assertEqual(constants.TEST_PASSWORD, user.password)


class ProfileModelTest(TestCase):
    """
    Profile Model Test
    """

    def setUp(self):
        """
        Test Set Up
        """

        self.user = User.objects.create(
            username=constants.TEST_USERNAME,
            email=constants.TEST_EMAIL,
            password=constants.TEST_PASSWORD
        )

    def test_create_and_save_profile(self):
        """
        Create Profile Model Test
        """

        profile = Profile.objects.get(user=self.user)
        profile.image = constants.TEST_IMAGE
        profile.bio = constants.TEST_BIO
        profile.save()

        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(self.user, profile.user)
        self.assertEqual(constants.TEST_IMAGE, profile.image)
        self.assertEqual(constants.TEST_BIO, profile.bio)


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
        Test Create and Save Friend Request Model
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
        Test Create and Save Friend Model
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
        """
        Test Create and Save User Drink Model
        """

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


class IngredientModelTest(TestCase):
    """
    Ingredient Model Test
    """

    # constants
    TEST_USERNAME = 'test_username'
    TEST_EMAIL = 'test_email'
    TEST_PASSWORD = 'test_password'
    TEST_DRINK_NAME = 'test_name'
    TEST_DRINK_DESCRIPTION = 'test_description'
    TEST_DRINK_TIMESTAMP = datetime.datetime(
        2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    TEST_DRINK_LIKES = 0
    TEST_DRINK_IMAGE = 'default.jpg'
    TEST_INGREDIENT_NAME = 'test_ingredient_name'
    TEST_INGREDIENT_QUANTITY = 'test_ingredient_quantity'

    def test_create_and_save_ingredient(self):
        """
        Test Create and Save Ingredient Model
        """

        mocked = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            user = User.objects.create(
                username=self.TEST_USERNAME, email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

            drink = UserDrink.objects.create(
                user=user, name=self.TEST_DRINK_NAME, description=self.TEST_DRINK_DESCRIPTION, likes=self.TEST_DRINK_LIKES, image=self.TEST_DRINK_IMAGE)

            ingredient = Ingredient.objects.create(
                drink=drink, name=self.TEST_INGREDIENT_NAME, quantity=self.TEST_INGREDIENT_QUANTITY)

            self.assertTrue(isinstance(ingredient, Ingredient))
            self.assertTrue(isinstance(ingredient.drink.user, User))
            self.assertTrue(isinstance(ingredient.drink, UserDrink))
            self.assertEquals(user, ingredient.drink.user)
            self.assertEquals(drink, ingredient.drink)
            self.assertEquals(self.TEST_INGREDIENT_NAME, ingredient.name)
            self.assertEquals(self.TEST_INGREDIENT_QUANTITY,
                              ingredient.quantity)


class InstructionModelTest(TestCase):
    """
    Instruction Model Test
    """

    # constants
    TEST_USERNAME = 'test_username'
    TEST_EMAIL = 'test_email'
    TEST_PASSWORD = 'test_password'
    TEST_DRINK_NAME = 'test_name'
    TEST_DRINK_DESCRIPTION = 'test_description'
    TEST_DRINK_TIMESTAMP = datetime.datetime(
        2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    TEST_DRINK_LIKES = 0
    TEST_DRINK_IMAGE = 'default.jpg'
    TEST_INSTRUCTION = 'test_instruction'

    def test_create_and_save_instruction(self):
        """
        Test Create and Save Instruction Model
        """

        mocked = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            user = User.objects.create(
                username=self.TEST_USERNAME, email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

            drink = UserDrink.objects.create(
                user=user, name=self.TEST_DRINK_NAME, description=self.TEST_DRINK_DESCRIPTION, likes=self.TEST_DRINK_LIKES, image=self.TEST_DRINK_IMAGE)

            instruction = Instruction.objects.create(
                drink=drink, instruction=self.TEST_INSTRUCTION)

            self.assertTrue(isinstance(instruction, Instruction))
            self.assertTrue(isinstance(instruction.drink.user, User))
            self.assertTrue(isinstance(instruction.drink, UserDrink))
            self.assertEquals(user, instruction.drink.user)
            self.assertEquals(drink, instruction.drink)
            self.assertEquals(self.TEST_INSTRUCTION, instruction.instruction)


class LikeUserDrinkTest(TestCase):
    """
    Like User Drink Model Test
    """

    # constants
    TEST_USERNAME = 'test_username'
    TEST_EMAIL = 'test_email'
    TEST_PASSWORD = 'test_password'
    TEST_PROFILE_BIO = 'test_bio'
    TEST_PROFILE_IMAGE = 'default.jpg'
    TEST_DRINK_NAME = 'test_name'
    TEST_DRINK_DESCRIPTION = 'test_description'
    TEST_DRINK_TIMESTAMP = datetime.datetime(
        2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    TEST_DRINK_LIKES = 0
    TEST_DRINK_IMAGE = 'default.jpg'

    def test_create_and_save_like_user_drink(self):
        """
        Test Create and Save Like User Drink Model
        """

        mocked = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            user = User.objects.create(
                username=self.TEST_USERNAME, email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

            profile = Profile.objects.get(user=user)
            profile.bio = self.TEST_PROFILE_BIO
            profile.image = self.TEST_PROFILE_IMAGE
            profile.save()

            drink = UserDrink.objects.create(
                user=user, name=self.TEST_DRINK_NAME, description=self.TEST_DRINK_DESCRIPTION, likes=self.TEST_DRINK_LIKES, image=self.TEST_DRINK_IMAGE)

            like_drink = LikeUserDrink.objects.create(
                drink=drink, profile=profile)

            self.assertTrue(isinstance(like_drink, LikeUserDrink))
            self.assertTrue(isinstance(like_drink.drink, UserDrink))
            self.assertTrue(isinstance(like_drink.profile, Profile))
            self.assertEquals(drink, like_drink.drink)
            self.assertEquals(profile, like_drink.profile)
