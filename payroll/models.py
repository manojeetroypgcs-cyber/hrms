from django.db import models
from employees.models import Employee


class Payslip(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PAID', 'Paid'),
    )

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='payslips'
    )
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()

    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pay_period_start']

    def gross_salary(self):
        return self.basic_salary + self.hra + self.allowances

    def net_pay(self):
        return self.gross_salary() - self.deductions

    def __str__(self):
        return f"{self.employee.employee_code} - {self.pay_period_start} to {self.pay_period_end}"