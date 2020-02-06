from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Drinks(models.Model):
    drink_hash = models.CharField(max_length=64)
    profiles_that_liked = models.ManyToManyField(Profile)

    def __str__(self):
        return str(self.drink_hash)


class Drink_names(models.Model):
    drink_hash_FK = models.ForeignKey(Drinks, on_delete=models.PROTECT)
    drink_name = models.CharField(max_length=32)

    def __str__(self):
        return str(drink_hash_FK.drink_hash) + ", " + str(drink_name)
