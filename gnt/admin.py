"""
Admin Site Module
"""

from django.contrib import admin
from .models import Profile, Drink, DrinkName, ProfileToLikedDrink, ProfileToDislikedDrink, Friend, FriendRequest, UpvotedUserDrink, DownvotedUserDrink, UserDrink

admin.site.register(Profile)
admin.site.register(Drink)
admin.site.register(DrinkName)
admin.site.register(ProfileToLikedDrink)
admin.site.register(ProfileToDislikedDrink)
admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(UpvotedUserDrink)
admin.site.register(DownvotedUserDrink)
admin.site.register(UserDrink)