# Generated by Django 3.0.2 on 2020-02-07 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gnt', '0004_drink_names_drinks_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drink_names',
            old_name='drink_hash_FK',
            new_name='drink_FK',
        ),
        migrations.RemoveField(
            model_name='drinks',
            name='drink_hash',
        ),
    ]