# Generated by Django 5.1.5 on 2025-01-22 21:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter an employee role (e.g. e-commerce, import & export)', max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the title of the task', max_length=500)),
                ('description', models.CharField(help_text='Enter a detailed description of the task', max_length=2000)),
                ('date_of_assignment', models.DateField(blank=True, help_text='Enter the date when the task was assigned', null=True)),
                ('deadline', models.DateField(blank=True, help_text='Enter the deadline for this task', null=True)),
                ('status', models.CharField(blank=True, choices=[('in progress', 'In Progress'), ('postponed', 'Postponed'), ('done', 'Done'), ('pending', 'Pending')], default='pending', help_text='Task progress status', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text="Enter the employee's first name", max_length=20)),
                ('last_name', models.CharField(help_text="Enter the employee's last name", max_length=20)),
                ('role', models.OneToOneField(help_text='Select a role for this employee', on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.role')),
            ],
        ),
    ]
