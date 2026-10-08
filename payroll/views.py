from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Payslip
from .forms import PayslipForm
from employees.models import Employee


@login_required
def payslip_list(request):
    if request.user.is_hr():
        payslips = Payslip.objects.select_related('employee__user').all()
    else:
        try:
            emp = request.user.employee
            payslips = Payslip.objects.filter(employee=emp)
        except Employee.DoesNotExist:
            payslips = Payslip.objects.none()

    return render(request, 'payroll/list.html', {'payslips': payslips})


@login_required
def payslip_detail(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)

    if not request.user.is_hr() and payslip.employee.user != request.user:
        messages.error(request, 'You can only view your own payslips.')
        return redirect('payslip_list')

    return render(request, 'payroll/detail.html', {'payslip': payslip})


@login_required
def payslip_create(request):
    if not request.user.is_hr():
        messages.error(request, 'Access denied. Only HR/Admin can create payslips.')
        return redirect('payslip_list')

    if request.method == 'POST':
        form = PayslipForm(request.POST)
        if form.is_valid():
            payslip = form.save()
            messages.success(request, 'Payslip created successfully.')
            return redirect('payslip_detail', pk=payslip.pk)
    else:
        form = PayslipForm()

    return render(request, 'payroll/create.html', {'form': form})


@login_required
def payslip_delete(request, pk):
    if not request.user.is_admin():
        messages.error(request, 'Only admin can delete payslips.')
        return redirect('payslip_list')

    payslip = get_object_or_404(Payslip, pk=pk)
    if request.method == 'POST':
        payslip.delete()
        messages.success(request, 'Payslip deleted.')
        return redirect('payslip_list')

    return render(request, 'payroll/confirm_delete.html', {'payslip': payslip})