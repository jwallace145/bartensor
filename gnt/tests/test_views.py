"""
Views Module Test
"""

# import necessary modules
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from gnt.tests import constants


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
            '/Users/jameswallace/Documents/Gin-and-Tensor/gnt/tests/chromedriver')

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
            '/Users/jameswallace/Documents/Gin-and-Tensor/gnt/tests/chromedriver')

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

    def test_profile_edit_success(self):
        """
        Successful Profile Edit Test
        """

        self.browser.get(self.live_server_url + '/profile-edit/')

        username = self.browser.find_element_by_id(constants.ID_USERNAME)
        email = self.browser.find_element_by_id(constants.ID_EMAIL)
        image = self.browser.find_element_by_id(constants.ID_IMAGE)
        bio = self.browser.find_element_by_id(constants.ID_BIO)
        update = self.browser.find_element_by_name(constants.UPDATE_BUTTON)

        username.clear()
        email.clear()
        bio.clear()

        username.send_keys(constants.TEST_USERNAME)
        email.send_keys(constants.TEST_EMAIL)
        # image.send_keys(constants.TEST_IMAGE)
        bio.send_keys(constants.TEST_BIO)
        update.send_keys(Keys.RETURN)

        user = User.objects.get(username=constants.TEST_USERNAME)

        self.assertTrue(isinstance(user, User))
        self.assertEquals(constants.TEST_USERNAME, user.username)
        self.assertEquals(constants.TEST_EMAIL, user.email)
        self.assertEquals(constants.TEST_BIO, user.profile.bio)
