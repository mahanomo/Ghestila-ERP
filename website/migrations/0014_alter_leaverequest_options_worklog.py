# Generated by Django 5.2.1 on 2025-05-31 08:29

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_alter_leaverequest_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaverequest',
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', django_jalali.db.models.jDateTimeField(blank=True, null=True)),
                ('end_time', django_jalali.db.models.jDateTimeField(blank=True, null=True)),
                ('report', models.TextField(blank=True, null=True)),
                ('date', django_jalali.db.models.jDateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
