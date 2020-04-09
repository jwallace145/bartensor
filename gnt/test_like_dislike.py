from django.test import TestCase
from django.contrib.auth.models import User
from gnt import models
from gnt.models import Profile, Drink


class TestLikes(TestCase):
    """
    Tests like drink functionality with DB
    """

    def create_test_Profile(self):
        self.test_user = User.objects.create_user('Tester')
        self.test_profile = models.Profile.objects.create(
            user=self.test_user, bio='test')

    def new_user_1_like(self):
        drink = Drink.objects.get(
            drink_hash='1b588790-9610-478c-8899-e700d33f6eb5')
        profile = Profile.objects.get(user=self.test_user)
