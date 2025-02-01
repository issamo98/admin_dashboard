from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employee, Task, Hour, Role
from django.http import Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
from django.db.models import Q
from .filters import HourFilter  # Import the filter class







@login_required
def dashboard_admin(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('login')

    if employee.role.is_manager:
        # Admin Dashboard
        employees = Employee.objects.all()

        paginate_by = 7  # Define how many items per page you want
        paginator = Paginator(employees, paginate_by)

        page = request.GET.get('page')  # Get the page number from the request
        try:
            paginated_employees = paginator.page(page)
        except PageNotAnInteger:
            paginated_employees = paginator.page(1)
        except EmptyPage:
            paginated_employees = paginator.page(paginator.num_pages)

        return render(request, 'dashboard_admin.html', {
            'employees': paginated_employees,  # Use the paginated data
        })
    elif employee.role.is_comptable:
        # Comptable Employee Dashboard
        tasks = Task.objects.filter(assign_to=employee)
        return render(request, 'dashboard_employeev2.html', {'tasks': tasks})
    else:
        # Employee Dashboard
        tasks = Task.objects.filter(assign_to=employee)
        return render(request, 'dashboard_employee.html', {'tasks': tasks})



@login_required
def trackhamza(request):


    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('login')

    if not employee.role.is_comptable:  # Restrict access to comptable employees only
        return redirect('dashboard_admin')


    hours = Hour.objects.select_related('employee').all()

    hour_filter = HourFilter(request.GET, queryset=hours)



    return render(request, 'track_hourshamza.html', {
        'hours': hours,
        'filter': hour_filter,

    })







@login_required
def add_employee(request):
    if not hasattr(request.user, 'employee') or not request.user.employee.role.is_manager:
        return redirect('dashboard_admin')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role_id = request.POST.get('role')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Create a new user if username and password are provided
            if username and password:
                user = User.objects.create_user(username=username, password=password)
            else:
                user = None

            # Assign role
            role = Role.objects.get(id=role_id)

            # Create the Employee
            Employee.objects.create(first_name=first_name, last_name=last_name, role=role, user=user)

            return redirect('dashboard_admin')
        except Role.DoesNotExist:
            return render(request, 'add_worker.html', {'error': 'Role does not exist'})

    roles = Role.objects.all()
    return render(request, 'add_employee.html', {'roles': roles})


@login_required
def add_task(request):
    if not hasattr(request.user, 'employee') or not request.user.employee.role.is_manager:
        return redirect('dashboard_admin')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        assign_to_id = request.POST.get('assign_to')

        assign_to = Employee.objects.get(id=assign_to_id)
        Task.objects.create(title=title, description=description, deadline=deadline, assign_to=assign_to)

        return redirect('dashboard_admin')

    employees = Employee.objects.all()
    return render(request, 'add_task.html', {'employees': employees})




@login_required
def manage_employee(request, employee_id):
    # Ensure the current user is a manager
    if not hasattr(request.user, 'employee') or not request.user.employee.role.is_manager:
        return redirect('dashboard_admin')

    # Get the employee to manage
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        raise Http404("Employee not found")

    # Get all tasks assigned to this employee
    tasks = Task.objects.filter(assign_to=employee)

    # Handle task deletion
    if 'delete_task' in request.POST:
        task_id = request.POST.get('task_id')
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('manage_employee', employee_id=employee.id)

    # Handle task status update
    if 'update_status' in request.POST:
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        task = Task.objects.get(id=task_id)
        task.status = status
        task.save()
        return redirect('manage_employee', employee_id=employee.id)

    # Handle employee deletion
    if 'delete_employee' in request.POST:
        employee.delete()
        return redirect('dashboard_admin')  # Or any other page you want to redirect to after deleting

    return render(request, 'manage_employee.html', {'employee': employee, 'tasks': tasks})



@login_required
def dashboard_employee(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('login')

    tasks = Task.objects.filter(assign_to=employee)

    if request.method == 'POST' and 'update_status' in request.POST:
        task_id = request.POST.get('task_id')
        new_status = request.POST.get('status')

        task = Task.objects.get(id=task_id)
        task.status = new_status
        task.save()
        return redirect('dashboard_employee')  # Refresh the page to show updated status

    return render(request, 'dashboard_employee.html', {'tasks': tasks})

@login_required
def employee_hours(request):


    """Employee view to manage their own hours."""
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return redirect('login')

    # Fetch the hours for the current employee
    hours = Hour.objects.filter(employee=employee)

    # Pagination
    paginate_by = 5  # Define how many items per page you want
    paginator = Paginator(hours, paginate_by)

    page = request.GET.get('page')  # Get the page number from the request
    try:
        paginated_hours = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paginated_hours = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        paginated_hours = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        # Add or update hours
        date = request.POST.get('date')
        entry_time = request.POST.get('entry_time')
        exit_time = request.POST.get('exit_time')

        if date and entry_time and exit_time:
            # Create a new hour entry for the employee
            Hour.objects.create(employee=employee, date=date, entry_time=entry_time, exit_time=exit_time)
            return redirect('employee_hours')  # Redirect to refresh the page

    return render(request, 'employee_hours.html', {'employee': employee,
                                                   'hours': paginated_hours,  # Use the paginated data
                                                   'paginator': paginator,  # Pass paginator for navigation controls
                                                   })




@login_required
def manage_employee_hours(request, employee_id):

    """Admin view to manage hours for a specific employee."""
    if not hasattr(request.user, 'employee') or not request.user.employee.role.is_manager:
        return redirect('dashboard_admin')

    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        raise Http404("Employee not found")

    hours = Hour.objects.filter(
        Q(employee=employee)

    )

    # Pagination
    paginate_by = 5  # Define how many items per page you want
    paginator = Paginator(hours, paginate_by)

    page = request.GET.get('page')  # Get the page number from the request
    try:
        paginated_hours = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paginated_hours = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        paginated_hours = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        # Add a new hour entry for the managed employee
        date = request.POST.get('date')
        entry_time = request.POST.get('entry_time')
        exit_time = request.POST.get('exit_time')

        if date and entry_time and exit_time:
            Hour.objects.create(employee=employee, date=date, entry_time=entry_time, exit_time=exit_time)
            return redirect('manage_employee_hours', employee_id=employee.id)

    return render(request, 'manage_employee_hours.html', {'employee': employee,
                                                          'hours': paginated_hours,  # Use the paginated data
                                                          'paginator': paginator,  # Pass paginator for navigation controls
                                                            })

@login_required
def edit_employee_hour(request, employee_id, hour_id):
    """Edit an employee's work hour entry."""


    # Get the employee and the specific Hour entry
    employee = get_object_or_404(Employee, id=employee_id)
    hour = get_object_or_404(Hour, id=hour_id)

    # Handle form submission for editing the hour entry
    if request.method == 'POST':
        date = request.POST.get('date')
        entry_time = request.POST.get('entry_time')
        exit_time = request.POST.get('exit_time')

        # Update the hour entry
        if date and entry_time and exit_time:
            hour.date = date
            hour.entry_time = entry_time
            hour.exit_time = exit_time
            hour.save()
            return redirect('manage_employee_hours', employee_id=employee.id)

    return render(request, 'edit_employee_hour.html', {'hour': hour, 'employee': employee})


@login_required
def delete_employee_hour(request, employee_id, hour_id):
    """Delete an employee's work hour entry."""




    # Get the employee and the specific Hour entry to delete
    employee = get_object_or_404(Employee, id=employee_id)
    hour = get_object_or_404(Hour, id=hour_id)

    # Handle the deletion of the hour entry
    if request.method == 'POST':
        hour.delete()
        return redirect('manage_employee_hours', employee_id=employee.id)

    return render(request, 'delete_employee_hour.html', {'hour': hour, 'employee': employee})
