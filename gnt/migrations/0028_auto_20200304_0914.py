# Generated by Django 3.0.3 on 2020-03-04 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gnt', '0027_user_drink_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_drink',
            old_name='drink_name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='user_drink',
            name='description',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user_drink',
            name='profile_FK',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gnt.Profile'),
            preserve_default=False,
        ),
    ]
