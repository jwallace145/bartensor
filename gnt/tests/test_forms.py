"""
Forms Test Module
"""

# import necessary modules
from django.contrib.auth.models import User
from django.test import TestCase
from gnt.forms import CreateUserDrinkForm, CreateUserDrinkIngredientForm, CreateUserDrinkInstructionForm, ProfileUpdateForm, UserRegisterForm, UserUpdateForm


class UserRegisterFormTest(TestCase):
    """
    User Register Form Test Class
    """

    # constants
    TEST_USERNAME = 'testuser'
    TEST_EXISTING_USERNAME = 'existinguser'
    TEST_EMAIL = 'testuser@email.com'
    TEST_PASSWORD = 'TestPassword123'
    TEST_INCORRECT_PASSWORD = 'TestPassword321'

    def setUp(self):
        """
        Test Set Up
        """

        # populate test database with an existing user
        User.objects.create(username=self.TEST_EXISTING_USERNAME,
                            email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

    def test_user_register_form_success(self):
        """
        User Register Form Test Success
        """

        form = UserRegisterForm(data={
            'username': self.TEST_USERNAME,
            'email': self.TEST_EMAIL,
            'password1': self.TEST_PASSWORD,
            'password2': self.TEST_PASSWORD
        })

        self.assertTrue(form.is_valid())

    def test_user_register_form_different_passwords(self):
        """
        User Register Form Test Failure Different Passwords
        """

        form = UserRegisterForm(data={
            'username': self.TEST_USERNAME,
            'email': self.TEST_EMAIL,
            'password1': self.TEST_PASSWORD,
            'password2': self.TEST_INCORRECT_PASSWORD
        })

        self.assertFalse(form.is_valid())

    def test_duplicate_user_register_form(self):
        """
        User Register Form Test Failure Duplicate Users
        """

        form = UserRegisterForm(data={
            'username': self.TEST_EXISTING_USERNAME,
            'email': self.TEST_EMAIL,
            'password1': self.TEST_PASSWORD,
            'password2': self.TEST_INCORRECT_PASSWORD
        })

        self.assertFalse(form.is_valid())


class UserUpdateFormTest(TestCase):
    """
    User Update Form Test Class
    """

    # constants
    TEST_USERNAME = 'testuser'
    TEST_EXISTING_USERNAME = 'existinguser'
    TEST_EMAIL = 'testuser@email.com'

    def test_user_update_form_success(self):
        """
        User Update Form Test Success
        """

        form = UserUpdateForm(data={
            'username': self.TEST_USERNAME,
            'email': self.TEST_EMAIL
        })

        self.assertTrue(form.is_valid())


class ProfileUpdateFormTest(TestCase):
    """
    Profile Update Form Test Class
    """

    # constants
    TEST_BIO = 'test bio'
    TEST_IMAGE = 'default.jpg'

    def test_profile_update_form_success(self):
        """
        Profile Update Form Test Success
        """

        form = ProfileUpdateForm(data={
            'image': self.TEST_IMAGE,
            'bio': self.TEST_BIO
        })

        self.assertTrue(form.is_valid())


class CreateUserDrinkFormTest(TestCase):
    """
    Create User Drink Form Test Class
    """

    # constants
    TEST_DRINK_NAME = 'test drink name'
    TEST_DRINK_DESCRIPTION = 'test drink description'
    TEST_DRINK_IMAGE = 'default.jpg'

    def test_create_user_drink_form_success(self):
        """
        Create User Drink Form Test Success
        """

        form = CreateUserDrinkForm(data={
            'name': self.TEST_DRINK_NAME,
            'description': self.TEST_DRINK_DESCRIPTION,
            'image': self.TEST_DRINK_IMAGE
        })

        self.assertTrue(form.is_valid())


class CreateUserDrinkIngredientFormTest(TestCase):
    """
    Create User Drink Ingredient Form Test Class
    """

    # constants
    TEST_USER_DRINK_INGREDIENT_NAME = 'test ingredient name'
    TEST_USER_DRINK_INGREDIENT_QUANTITY = 'test ingredient quantity'

    def test_create_user_drink_ingredient_form_success(self):
        """
        Create User Drink Ingredient Form Test Success
        """

        form = CreateUserDrinkIngredientForm(data={
            'name': self.TEST_USER_DRINK_INGREDIENT_NAME,
            'quantity': self.TEST_USER_DRINK_INGREDIENT_QUANTITY
        })

        self.assertTrue(form.is_valid())


class CreateUserDrinkInstructionFormTest(TestCase):
    """
    Create User Drink Instruction Form Test Class
    """

    # constants
    TEST_USER_DRINK_INSTRUCTION = 'test instruction'

    def test_create_user_drink_instruction_form_success(self):
        """
        Create User Drink Instruction Form Test Success
        """

        form = CreateUserDrinkInstructionForm(data={
            'instruction': self.TEST_USER_DRINK_INSTRUCTION
        })

        self.assertTrue(form.is_valid())
