# Generated by Django 3.0.3 on 2020-03-06 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnt', '0034_user_drink_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='UserDrink',
            name='image',
            field=models.ImageField(
                default='default.jpg', upload_to='user_drink_pics'),
        ),
    ]
