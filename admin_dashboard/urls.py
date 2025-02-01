from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static# Import LogoutView here

from . import views  # Import custom views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('add_task/', views.add_task, name='add_task'),  # Add the URL pattern for add_task
    path('manage_employee/<int:employee_id>/', views.manage_employee, name='manage_employee'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Use auth_views for LogoutView
    path('employee/hours/', views.employee_hours, name='employee_hours'),
    path('manage-hours/<int:employee_id>/', views.manage_employee_hours, name='manage_employee_hours'),
    path('employee/<int:employee_id>/hours/edit/<int:hour_id>/', views.edit_employee_hour, name='edit_employee_hour'),
    path('employee/<int:employee_id>/hours/delete/<int:hour_id>/', views.delete_employee_hour, name='delete_employee_hour'),
    path('employee/hours/', views.employee_hours, name='employee_hours'),
    path('employee/hours/edit/<int:hour_id>/', views.edit_employee_hour, name='edit_employee_hour'),
    path('comptable/hours/', views.trackhamza, name='trackhamza'),
]


"""make some"""