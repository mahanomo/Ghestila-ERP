# Generated by Django 5.2.1 on 2025-05-31 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_alter_leaverequest_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaverequest',
            options={'ordering': ['created_at']},
        ),
    ]
