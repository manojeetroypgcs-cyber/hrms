from django.db import models
from employees.models import Employee


class Attendance(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='attendance_records'
    )
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    work_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.employee.employee_code} - {self.date}"

    def calculate_hours(self):
        if self.check_in and self.check_out:
            from datetime import datetime, date as date_cls
            in_dt = datetime.combine(date_cls.today(), self.check_in)
            out_dt = datetime.combine(date_cls.today(), self.check_out)
            diff = (out_dt - in_dt).total_seconds() / 3600
            return round(diff, 2)
        return 0