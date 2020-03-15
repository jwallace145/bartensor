from django.test import TestCase
from django.contrib.auth.models import User
from gnt.models import Profile


# profile model test
class ProfileTest(TestCase):

    def create_user(self, username='test_username', email='test_email'):
        return User.create(username=username, email=email)

    def create_profile(self, user, image, bio)
    return 1
