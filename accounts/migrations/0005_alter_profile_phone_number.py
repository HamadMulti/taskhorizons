# Generated by Django 4.2.20 on 2025-04-12 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_access_expires_profile_free_access_start_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]
