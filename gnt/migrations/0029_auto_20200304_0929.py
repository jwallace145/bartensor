# Generated by Django 3.0.3 on 2020-03-04 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gnt', '0028_auto_20200304_0914'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='ingredient_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='ingredient_quantity',
            new_name='quantity',
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='user_drink_FK',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='gnt.User_drink'),
            preserve_default=False,
        ),
    ]
