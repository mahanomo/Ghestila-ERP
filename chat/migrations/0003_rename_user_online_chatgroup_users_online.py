# Generated by Django 5.2.1 on 2025-06-07 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatgroup_user_online'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatgroup',
            old_name='user_online',
            new_name='users_online',
        ),
    ]
