from django.contrib import admin
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'applied_at')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__employee_code', 'employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'applied_at'