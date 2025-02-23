# Generated by Django 5.1.5 on 2025-01-26 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0002_employee_user_role_is_manager_task_assign_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_time', models.TimeField(blank=True, help_text='Enter the time when you entered the desk', null=True)),
                ('exit_time', models.TimeField(blank=True, help_text='Enter the time when you exited the desk', null=True)),
                ('date', models.DateField(help_text='Enter the date for this work entry')),
                ('employee', models.ForeignKey(help_text='The employee linked to these hours', on_delete=django.db.models.deletion.CASCADE, related_name='hours', to='admin_dashboard.employee')),
            ],
            options={
                'verbose_name': 'Work Hour',
                'verbose_name_plural': 'Work Hours',
                'ordering': ['-date'],
            },
        ),
    ]
