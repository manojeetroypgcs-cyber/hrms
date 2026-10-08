from django.contrib import admin
from .models import Payslip


@admin.register(Payslip)
class PayslipAdmin(admin.ModelAdmin):
    list_display = ('employee', 'pay_period_start', 'pay_period_end', 'net_pay', 'status')
    list_filter = ('status', 'pay_period_start')
    search_fields = ('employee__employee_code', 'employee__user__first_name', 'employee__user__last_name')
    date_hierarchy = 'pay_period_start'