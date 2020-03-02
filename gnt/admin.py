from django.contrib import admin
from .models import Profile, Drinks, Drink_names, Profile_to_liked_drink, Profile_to_disliked_drink, Friend, Friend_request

admin.site.register(Profile)
admin.site.register(Drinks)
admin.site.register(Drink_names)
admin.site.register(Profile_to_liked_drink)
admin.site.register(Profile_to_disliked_drink)
admin.site.register(Friend)
admin.site.register(Friend_request)

