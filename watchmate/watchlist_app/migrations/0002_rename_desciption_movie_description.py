# Generated by Django 4.0.4 on 2022-05-06 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='desciption',
            new_name='description',
        ),
    ]
