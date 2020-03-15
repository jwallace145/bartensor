from django.contrib import admin
from .models import Profile, Drink, DrinkName, ProfileToLikedDrink, ProfileToDislikedDrink, Friend, FriendRequest

admin.site.register(Profile)
admin.site.register(Drink)
admin.site.register(DrinkName)
admin.site.register(ProfileToLikedDrink)
admin.site.register(ProfileToDislikedDrink)
admin.site.register(Friend)
admin.site.register(FriendRequest)
