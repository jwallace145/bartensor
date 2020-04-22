"""
Views Module Test
"""

import time

# import necessary modules
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from gnt.tests import constants
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class RegisterUserViewTest(StaticLiveServerTestCase):
    """
    Register User View Test
    """

    # selenium browser port
    port = 8081

    def setUp(self):
        """
        Test Set Up
        """

        self.browser = webdriver.Chrome(
            '/Users/jameswallace/Documents/bartensor/gnt/tests/chromedriver')

    def tearDown(self):
        """
        Test Tear Down
        """

        self.browser.quit()

    def test_register_new_user_success(self):
        """
        Successful Register a New User Test
        """

        self.browser.get(self.live_server_url + '/register')

        username = self.browser.find_element_by_id(constants.ID_USERNAME)
        email = self.browser.find_element_by_id(constants.ID_EMAIL)
        password1 = self.browser.find_element_by_id(constants.ID_PASSWORD1)
        password2 = self.browser.find_element_by_id(constants.ID_PASSWORD2)
        register = self.browser.find_element_by_name(constants.REGISTER_BUTTON)

        username.send_keys(constants.TEST_USERNAME)
        email.send_keys(constants.TEST_EMAIL)
        password1.send_keys(constants.TEST_PASSWORD)
        password2.send_keys(constants.TEST_PASSWORD)
        register.send_keys(Keys.RETURN)

        user = User.objects.get(username=constants.TEST_USERNAME)

        self.assertTrue(isinstance(user, User))
        self.assertEquals(constants.TEST_USERNAME, user.username)
        self.assertEquals(constants.TEST_EMAIL, user.email)


class ProfileEditViewTest(StaticLiveServerTestCase):
    """
    Profile Edit View Test
    """

    # selenium browser port
    port = 8081

    def setUp(self):
        """
        Test Set Up
        """

        self.browser = webdriver.Chrome(
            '/Users/jameswallace/Documents/bartensor/gnt/tests/chromedriver')

        # populate test database with an existing user
        self.user = User.objects.create(
            username=constants.TEST_EXISTING_USERNAME,
            email=constants.TEST_EXISTING_EMAIL,
            password=constants.TEST_PASSWORD
        )

        self.client = Client()
        self.client.force_login(self.user)
        cookie = self.client.cookies['sessionid']

        self.browser.get(self.live_server_url)
        self.browser.add_cookie({
            'name': 'sessionid',
            'value': cookie.value,
            'secure': False,
            'path': '/'
        })

    def tearDown(self):
        """
        Test Tear Down
        """

        self.browser.quit()
