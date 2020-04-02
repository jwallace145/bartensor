"""
Models Module
"""

# import necessary modules
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    """
    Profile Model Class
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=250, default='insert bio here...')

    def __str__(self):
        return f'{ self.user.username } profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        # resize profile picture
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class FriendRequest(models.Model):
    """
    Friend Request Model Class
    """

    requestee = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name='profilerequest1')
    requestor = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name='profilerequest2')

    def __str__(self):
        return str(self.requestor) + ' friend requested ' + str(self.requestee)


class Friend(models.Model):
    """
    Friend Model Class
    """

    friend1 = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name='profile1')
    friend2 = models.ForeignKey(
        Profile, on_delete=models.PROTECT, related_name='profile2')

    def __str__(self):
        return str(self.friend1) + " is friends with " + str(self.friend2)


class Drink(models.Model):
    """
    Drink Model Class
    """

    drink_hash = models.CharField(
        max_length=64, default='emptydrink', unique=True)
    image = models.ImageField(default='default.jpg', upload_to='drink_pics')

    def __str__(self):
        return str(self.id) + ', ' + str(self.drink_hash)


class DrinkName(models.Model):
    """
    Drink Name Model Class
    """

    drink = models.ForeignKey(Drink, on_delete=models.PROTECT)
    drink_name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.id) + ', ' + str(self.drink.drink_hash) + ', ' + str(self.drink_name)


class ProfileToLikedDrink(models.Model):
    """
    Profile to Liked Drink Model Class
    """

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + ', ' + str(self.profile.user.username) + ', ' + str(self.drink.drink_hash)


class ProfileToDislikedDrink(models.Model):
    """
    Profile to Disliked Drink Model Class
    """

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    drink = models.ForeignKey(Drink, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + ', ' + str(self.profile.user.username) + ', ' + str(self.drink.drink_hash)


class UserDrink(models.Model):
    """
    User Drink Model Class
    """

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    image = models.ImageField(default='default.jpg',
                              upload_to='user_drink_pics')


class Ingredient(models.Model):
    """
    Ingredient Model Class
    """

    drink = models.ForeignKey(UserDrink, on_delete=models.PROTECT)
    name = models.CharField(max_length=32)
    quantity = models.CharField(max_length=32)

    def __str__(self):
        return str(self.id) + ', ' + str(self.drink.name) + ', ' + str(self.name) + ', ' + str(self.quantity)


class Instruction(models.Model):
    """
    Instruction Model Class
    """

    drink = models.ForeignKey(UserDrink, on_delete=models.PROTECT)
    instruction = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id) + ', ' + str(self.drink.name) + ', ' + str(self.instruction)


class UpvotedUserDrink(models.Model):
    """
    Upvoted User Drink Model class
    """

    drink = models.ForeignKey(UserDrink, on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + ', ' + str(self.drink) + ', ' + str(self.profile)


class DownvotedUserDrink(models.Model):
    """
    Downvoted User Drink Model class
    """

    drink = models.ForeignKey(UserDrink, on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id) + ', ' + str(self.drink) + ', ' + str(self.profile)

