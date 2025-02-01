from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.exceptions import ValidationError
import django_filters


class Role(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter an employee role (e.g. e-commerce, import & export)"
    )
    is_manager = models.BooleanField(default=False, help_text="Check if this role is managerial")
    is_comptable = models.BooleanField(default=False, help_text="Check if this role is : comptable")

    def __str__(self):
        """String for representing the Model object."""
        return self.name



class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, help_text="Link to the Django user", null=True, blank=True
    )
    first_name = models.CharField(max_length=20, help_text="Enter the employee's first name")
    last_name = models.CharField(max_length=20, help_text="Enter the employee's last name")
    role = models.OneToOneField(
        Role,
        on_delete=models.CASCADE,  # Specify the behavior when the related Role is deleted
        help_text="Select a role for this employee"
    )

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'




class Task(models.Model):
    title = models.CharField(max_length=500, help_text="Enter the title of the task")
    description = models.CharField(max_length=2000, help_text="Enter a detailed description of the task")
    date_of_assignment = models.DateField(
        null=True,
        blank=True,
        help_text="Enter the date when the task was assigned"
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        help_text="Enter the deadline for this task"
    )

    TASK_STATUS = (
        ('in progress', 'In Progress'),
        ('postponed', 'Postponed'),
        ('done', 'Done'),
        ('pending', 'Pending'),
    )

    status = models.CharField(
        max_length=15,  # Increased to accommodate the longest choice ('in progress')
        choices=TASK_STATUS,
        blank=True,
        default='pending',
        help_text="Task progress status",
    )

    assign_to = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,  # Specify the behavior when the related Role is deleted
        help_text="Select a role for this employee"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Hour(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        help_text="The employee linked to these hours",
        related_name="hours"
    )
    entry_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Enter the time when you entered the desk"
    )
    exit_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Enter the time when you exited the desk"
    )
    date = models.DateField(
        help_text="Enter the date for this work entry"
    )
    def clean(self):
        """Custom validation for the model."""
        if self.entry_time and self.exit_time:
            if self.exit_time <= self.entry_time:
                raise ValidationError("Exit time must be later than entry time.")

    def total_hours(self):
        """Calculate the total time worked."""
        if self.entry_time and self.exit_time:
            entry = timedelta(
                hours=self.entry_time.hour, minutes=self.entry_time.minute, seconds=self.entry_time.second
            )
            exit = timedelta(
                hours=self.exit_time.hour, minutes=self.exit_time.minute, seconds=self.exit_time.second
            )
            return exit - entry
        return timedelta(0)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.employee} - {self.date}"

    class Meta:
        verbose_name = "Work Hour"
        verbose_name_plural = "Work Hours"
        ordering = ["-date"]


