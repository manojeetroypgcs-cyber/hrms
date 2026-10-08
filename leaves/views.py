from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import LeaveRequest
from .forms import LeaveRequestForm
from employees.models import Employee


@login_required
def apply_leave(request):
    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, 'You do not have an employee profile.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = emp
            leave.save()
            messages.success(request, 'Leave request submitted successfully.')
            return redirect('my_leaves')
    else:
        form = LeaveRequestForm()

    return render(request, 'leaves/apply.html', {'form': form})


@login_required
def my_leaves(request):
    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        messages.warning(request, 'You do not have an employee profile.')
        return redirect('dashboard')

    leaves = LeaveRequest.objects.filter(employee=emp)
    return render(request, 'leaves/my_leaves.html', {'leaves': leaves})


@login_required
def pending_leaves(request):
    if not request.user.is_manager():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    leaves = LeaveRequest.objects.filter(status='PENDING').select_related(
        'employee__user', 'employee__department'
    )
    return render(request, 'leaves/pending.html', {'leaves': leaves})


@login_required
def approve_leave(request, pk):
    if not request.user.is_manager():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'APPROVED'
    try:
        leave.approved_by = request.user.employee
    except Employee.DoesNotExist:
        pass
    leave.remarks = request.POST.get('remarks', '')
    leave.save()
    messages.success(request, 'Leave approved.')
    return redirect('pending_leaves')


@login_required
def reject_leave(request, pk):
    if not request.user.is_manager():
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    leave = get_object_or_404(LeaveRequest, pk=pk)
    leave.status = 'REJECTED'
    try:
        leave.approved_by = request.user.employee
    except Employee.DoesNotExist:
        pass
    leave.remarks = request.POST.get('remarks', '')
    leave.save()
    messages.success(request, 'Leave rejected.')
    return redirect('pending_leaves')