# Generated by Django 3.0.3 on 2020-03-15 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gnt', '0037_likeuserdrink'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdrink',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
