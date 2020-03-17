"""
Forms Test Module
"""

# import necessary modules
from django.contrib.auth.models import User
from django.test import TestCase
from gnt.forms import CreateUserDrinkForm
from gnt.forms import CreateUserDrinkIngredientForm
from gnt.forms import CreateUserDrinkInstructionForm
from gnt.forms import ProfileUpdateForm
from gnt.forms import UserRegisterForm
from gnt.forms import UserUpdateForm
from gnt.models import Ingredient
from gnt.models import Instruction
from gnt.models import Profile
from gnt.models import UserDrink
from gnt.tests import constants


class CreateUserDrinkFormTest(TestCase):
    """
    Create User Drink Form Test Class
    """

    def setUp(self):
        """
        Test Set Up
        """

        # populate test database with an existing user
        User.objects.create(
            username=constants.TEST_EXISTING_USERNAME,
            email=constants.TEST_EMAIL,
            password=constants.TEST_PASSWORD
        )

    def test_create_user_drink_form_success(self):
        """
        Successful Create User Drink Form Test
        """

        # create user drink form
        form = CreateUserDrinkForm(data={
            'name': constants.TEST_DRINK_NAME,
            'description': constants.TEST_DRINK_DESCRIPTION,
            'image': constants.TEST_DRINK_IMAGE
        })

        # assert the form is valid
        self.assertTrue(form.is_valid())

        # save the user drink with the form data and referenced user
        drink = form.save(commit=False)
        user = User.objects.get(username=constants.TEST_EXISTING_USERNAME)
        drink.user = user
        drink.save()

        # assert the drink fields are equal to the test constants
        self.assertTrue(isinstance(drink, UserDrink))
        self.assertEquals(user, drink.user)
        self.assertEquals(constants.TEST_DRINK_NAME, drink.name)
        self.assertEquals(constants.TEST_DRINK_DESCRIPTION, drink.description)
        self.assertEquals(constants.TEST_DRINK_IMAGE, drink.image)


class CreateUserDrinkIngredientFormTest(TestCase):
    """
    Create User Drink Ingredient Form Test Class
    """

    def setUp(self):
        """
        Test Set Up
        """

        # populate test database with an existing user
        User.objects.create(
            username=constants.TEST_EXISTING_USERNAME,
            email=constants.TEST_EMAIL,
            password=constants.TEST_PASSWORD
        )

    def test_create_user_drink_ingredient_form_success(self):
        """
        Successful Create User Drink Ingredient Form Test
        """

        # create user drink ingredient form
        form = CreateUserDrinkIngredientForm(data={
            'name': constants.TEST_USER_DRINK_INGREDIENT_NAME,
            'quantity': constants.TEST_USER_DRINK_INGREDIENT_QUANTITY
        })

        # assert the form is valid
        self.assertTrue(form.is_valid())


class CreateUserDrinkInstructionFormTest(TestCase):
    """
    Create User Drink Instruction Form Test Class
    """

    def setUp(self):
        """
        Test Set Up
        """

        # populate test database with an existing user
        User.objects.create(
            username=constants.TEST_EXISTING_USERNAME,
            email=constants.TEST_EMAIL,
            password=constants.TEST_PASSWORD
        )

    def test_create_user_drink_instruction_form_success(self):
        """
        Successful Create User Drink Instruction Form Test
        """

        # create user drink instruction form
        form = CreateUserDrinkInstructionForm(data={
            'instruction': constants.TEST_USER_DRINK_INSTRUCTION
        })

        # assert the form is valid
        self.assertTrue(form.is_valid())


class ProfileUpdateFormTest(TestCase):
    """
    Profile Update Form Test Class
    """

    def setUp(self):
        """
        Test Set Up
        """

        # populate test database with an existing user
        User.objects.create(
            username=constants.TEST_EXISTING_USERNAME,
            email=constants.TEST_EMAIL,
            password=constants.TEST_PASSWORD
        )

    def test_profile_update_form_success(self):
        """
        Profile Update Form Test Success
        """

        # create profile update form
        form = ProfileUpdateForm(data={
            'image': constants.TEST_IMAGE,
            'bio': constants.TEST_BIO
        })

        # assert the form is valid
        self.assertTrue(form.is_valid())


class UserRegisterFormTest(TestCase):
    """
    User Register Form Test Class
    """

    def setUp(self):
        """
        Test Set Up
        """

        # populate test database with an existing user
        User.objects.create(
            username=constants.TEST_EXISTING_USERNAME,
            email=constants.TEST_EMAIL,
            password=constants.TEST_PASSWORD
        )

    def test_user_register_form_success(self):
        """
        Successful User Register Form Test
        """

        # create user register form
        form = UserRegisterForm(data={
            'username': constants.TEST_USERNAME,
            'email': constants.TEST_EMAIL,
            'password1': constants.TEST_PASSWORD,
            'password2': constants.TEST_PASSWORD
        })

        # assert the form is valid
        self.assertTrue(form.is_valid())

    def test_user_register_form_different_passwords(self):
        """
        User Register Form Different Passwords Test
        """

        # create user register form
        form = UserRegisterForm(data={
            'username': constants.TEST_USERNAME,
            'email': constants.TEST_EMAIL,
            'password1': constants.TEST_PASSWORD,
            'password2': constants.TEST_INCORRECT_PASSWORD
        })

        # assert the form is not valid
        self.assertFalse(form.is_valid())

    def test_duplicate_user_register_form(self):
        """
        User Register Form Existing User Test
        """

        # create user register form
        form = UserRegisterForm(data={
            'username': constants.TEST_EXISTING_USERNAME,
            'email': constants.TEST_EMAIL,
            'password1': constants.TEST_PASSWORD,
            'password2': constants.TEST_PASSWORD
        })

        # assert the form is not valid
        self.assertFalse(form.is_valid())


class UserUpdateFormTest(TestCase):
    """
    User Update Form Test Class
    """

    def setUp(self):
        """
        Test Set Up
        """

        # populate test database with an existing user
        User.objects.create(
            username=constants.TEST_EXISTING_USERNAME,
            email=constants.TEST_EMAIL,
            password=constants.TEST_PASSWORD
        )

    def test_user_update_form_success(self):
        """
        Successful User Update Form Test
        """

        # create user update form
        form = UserUpdateForm(data={
            'username': constants.TEST_USERNAME,
            'email': constants.TEST_EMAIL
        })

        # assert the form is valid
        self.assertTrue(form.is_valid())

        # save the form
        form.save()

        # retrieve updated user
        user = User.objects.get(username=constants.TEST_USERNAME)

        # assert the updated user fields are equal to the test constants
        self.assertTrue(isinstance(user, User))
        self.assertEquals(constants.TEST_USERNAME, user.username)
        self.assertEquals(constants.TEST_EMAIL, user.email)

    def test_user_update_form_existing_user(self):
        """
        User Update Form Existing User Test
        """

        # create user update form
        form = UserUpdateForm(data={
            'username': constants.TEST_EXISTING_USERNAME,
            'email': constants.TEST_EMAIL
        })

        # assert the form is not valid
        self.assertFalse(form.is_valid())
