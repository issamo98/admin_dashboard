from django.contrib import admin
from .models import Role, Employee, Task, Hour




# Register your models here.
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Hour)