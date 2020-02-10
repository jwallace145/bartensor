from django.contrib import admin
from .models import Profile, Drinks, Drink_names, Profile_to_drink

admin.site.register(Profile)
admin.site.register(Drinks)
admin.site.register(Drink_names)
admin.site.register(Profile_to_drink)

