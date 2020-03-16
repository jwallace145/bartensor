"""
Views Module Test
"""

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
import time


class RegisterNewUserTest(StaticLiveServerTestCase):
    """
    Register New User Test
    """
    port = 8081

    # constants
    TEST_USERNAME = 'testuser'
    TEST_EMAIL = 'email@email.com'
    TEST_PASSWORD = 'TestPassword123'

    def setUp(self):
        self.browser = webdriver.Chrome(
            '/Users/jameswallace/Documents/Gin-and-Tensor/gnt/tests/chromedriver')

    def tearDown(self):
        self.browser.quit()

    def test_register_new_user(self):
        """
        Test Register a New User
        """

        self.browser.get(self.live_server_url + '/register')

        username = self.browser.find_element_by_id('id_username')
        email = self.browser.find_element_by_id('id_email')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')

        register = self.browser.find_element_by_name('register')

        username.send_keys(self.TEST_USERNAME)
        email.send_keys(self.TEST_EMAIL)
        password1.send_keys(self.TEST_PASSWORD)
        password2.send_keys(self.TEST_PASSWORD)

        register.send_keys(Keys.RETURN)

        user = User.objects.get(username=self.TEST_USERNAME)

        self.assertTrue(isinstance(user, User))
        self.assertEquals(self.TEST_USERNAME, user.username)
        self.assertEquals(self.TEST_EMAIL, user.email)
