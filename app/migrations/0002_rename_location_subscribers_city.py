# Generated by Django 4.1.7 on 2023-03-02 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscribers',
            old_name='location',
            new_name='city',
        ),
    ]
