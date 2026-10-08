from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from employees.models import Employee, Department
from attendance.models import Attendance
from leaves.models import LeaveRequest


@login_required
def dashboard(request):
    today = timezone.localdate()
    context = {
        'total_employees': Employee.objects.exclude(
    employment_status__in=['RESIGNED', 'TERMINATED']
).count(),
        'present_today': Attendance.objects.filter(date=today, check_in__isnull=False).count(),
        'pending_leaves': LeaveRequest.objects.filter(status='PENDING').count(),
        'total_departments': Department.objects.count(),
    }
    return render(request, 'dashboard.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
    path('leaves/', include('leaves.urls')),
    path('payroll/', include('payroll.urls')),
    path('performance/', include('performance.urls')),
    path('recruitment/', include('recruitment.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)