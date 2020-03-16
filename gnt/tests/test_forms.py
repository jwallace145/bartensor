"""
Forms Module Test
"""

# import necessary modules
from django.test import TestCase
from gnt.forms import UserRegisterForm
from django.contrib.auth.models import User


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
        User.objects.create(username=self.TEST_EXISTING_USERNAME,
                            email=self.TEST_EMAIL, password=self.TEST_PASSWORD)

    def test_user_register_form_success(self):
        form = UserRegisterForm(data={
            'username': self.TEST_USERNAME,
            'email': self.TEST_EMAIL,
            'password1': self.TEST_PASSWORD,
            'password2': self.TEST_PASSWORD
        })

        self.assertTrue(form.is_valid())

    def test_user_register_form_different_passwords(self):
        form = UserRegisterForm(data={
            'username': self.TEST_USERNAME,
            'email': self.TEST_EMAIL,
            'password1': self.TEST_PASSWORD,
            'password2': self.TEST_INCORRECT_PASSWORD
        })

        self.assertFalse(form.is_valid())

    def test_duplicate_user_register_form(self):
        form = UserRegisterForm(data={
            'username': self.TEST_EXISTING_USERNAME,
            'email': self.TEST_EMAIL,
            'password1': self.TEST_PASSWORD,
            'password2': self.TEST_INCORRECT_PASSWORD
        })

        self.assertFalse(form.is_valid())
