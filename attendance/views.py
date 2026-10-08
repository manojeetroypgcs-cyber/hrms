from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Attendance
from employees.models import Employee


@login_required
def attendance_list(request):
    if request.user.is_hr():
        records = Attendance.objects.select_related(
            'employee__user', 'employee__department'
        ).all()[:200]
    else:
        try:
            emp = request.user.employee
            records = Attendance.objects.filter(employee=emp)
        except Employee.DoesNotExist:
            records = Attendance.objects.none()
            messages.warning(request, 'You do not have an employee profile.')

    today = timezone.localdate()
    today_record = None
    try:
        emp = request.user.employee
        today_record = Attendance.objects.filter(employee=emp, date=today).first()
    except Employee.DoesNotExist:
        pass

    return render(request, 'attendance/list.html', {
        'records': records,
        'today_record': today_record,
        'today': today,
    })


@login_required
def check_in(request):
    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, 'You do not have an employee profile.')
        return redirect('attendance_list')

    today = timezone.localdate()
    att, created = Attendance.objects.get_or_create(employee=emp, date=today)

    if att.check_in:
        messages.info(request, 'You have already checked in today.')
    else:
        att.check_in = timezone.localtime(timezone.now()).time()
        att.save()
        messages.success(request, f'Checked in at {att.check_in.strftime("%H:%M:%S")}')

    return redirect('attendance_list')


@login_required
def check_out(request):
    try:
        emp = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, 'You do not have an employee profile.')
        return redirect('attendance_list')

    today = timezone.localdate()
    att = Attendance.objects.filter(employee=emp, date=today).first()

    if not att or not att.check_in:
        messages.error(request, 'You need to check in first.')
        return redirect('attendance_list')

    if att.check_out:
        messages.info(request, 'You have already checked out today.')
    else:
        att.check_out = timezone.localtime(timezone.now()).time()
        att.work_hours = att.calculate_hours()
        att.save()
        messages.success(request, f'Checked out at {att.check_out.strftime("%H:%M:%S")}. Hours: {att.work_hours}')

    return redirect('attendance_list')