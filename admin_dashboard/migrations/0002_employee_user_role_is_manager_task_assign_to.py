# Generated by Django 5.1.5 on 2025-01-23 10:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(blank=True, help_text='Link to the Django user', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='role',
            name='is_manager',
            field=models.BooleanField(default=False, help_text='Check if this role is managerial'),
        ),
        migrations.AddField(
            model_name='task',
            name='assign_to',
            field=models.ForeignKey(default=1, help_text='Select a role for this employee', on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.employee'),
            preserve_default=False,
        ),
    ]
