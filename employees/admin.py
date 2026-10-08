from django.contrib import admin
from .models import Employee, Department, Designation, EmployeeFamily, EmployeeDocument


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'level')
    list_filter = ('department',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_code', 'user', 'department', 'designation', 'employment_status', 'hire_date')
    list_filter = ('employment_status', 'department', 'designation')
    search_fields = ('employee_code', 'user__first_name', 'user__last_name', 'user__email')


@admin.register(EmployeeFamily)
class EmployeeFamilyAdmin(admin.ModelAdmin):
    list_display = ('employee', 'full_name', 'relationship')
    list_filter = ('relationship',)


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'uploaded_at')