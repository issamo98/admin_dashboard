import django_filters
from .models import Hour

class HourFilter(django_filters.FilterSet):
    employee = django_filters.CharFilter(field_name='employee__first_name', lookup_expr='icontains', label="Employee Name")
    date = django_filters.DateFromToRangeFilter(field_name='date', label="Date Range")


    class Meta:
        model = Hour
        fields = ['employee', 'date']
