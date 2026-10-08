from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Employee, EmployeeFamily
from .forms import EmployeeForm, EmployeeFamilyForm


@login_required
def employee_list(request):
    query = request.GET.get('q', '')
    employees = Employee.objects.select_related('user', 'department', 'designation').all()

    if query:
        employees = employees.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(employee_code__icontains=query) |
            Q(user__email__icontains=query)
        )

    return render(request, 'employees/employee_list.html', {
        'employees': employees,
        'query': query,
    })


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/employee_detail.html', {'employee': employee})


@login_required
def employee_create(request):
    if not request.user.is_hr():
        messages.error(request, 'Access denied. Only HR/Admin can create employees.')
        return redirect('employee_list')

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.employee_code} created successfully')
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee',
    })


@login_required
def employee_edit(request, pk):
    if not request.user.is_hr():
        messages.error(request, 'Access denied.')
        return redirect('employee_list')

    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully')
            return redirect('employee_detail', pk=pk)
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': f'Edit Employee: {employee.employee_code}',
    })


@login_required
def employee_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, 'Access denied. Only admin can delete employees.')
        return redirect('employee_list')

    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted')
        return redirect('employee_list')

    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


@login_required
def add_family_member(request, pk):
    if not request.user.is_hr():
        messages.error(request, 'Access denied.')
        return redirect('employee_detail', pk=pk)

    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeFamilyForm(request.POST)
        if form.is_valid():
            fam = form.save(commit=False)
            fam.employee = employee
            fam.save()
            messages.success(request, 'Family member added')
            return redirect('employee_detail', pk=pk)
    else:
        form = EmployeeFamilyForm()

    return render(request, 'employees/family_form.html', {'form': form, 'employee': employee})