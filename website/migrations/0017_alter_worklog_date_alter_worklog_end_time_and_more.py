# Generated by Django 5.2.1 on 2025-06-01 07:42

import datetime
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_alter_worklog_date_alter_worklog_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='date',
            field=django_jalali.db.models.jDateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='end_time',
            field=django_jalali.db.models.jDateTimeField(null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worklog',
            name='start_time',
            field=django_jalali.db.models.jDateTimeField(null=True, blank=True),
            preserve_default=False,
        ),
    ]
