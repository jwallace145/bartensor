# Generated by Django 3.0.3 on 2020-03-15 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gnt', '0040_merge_20200315_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdrink',
            name='likes',
        ),
    ]
