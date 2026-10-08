from django import forms
from .models import Payslip


class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = [
            'employee', 'pay_period_start', 'pay_period_end',
            'basic_salary', 'hra', 'allowances', 'deductions',
            'status', 'notes',
        ]
        widgets = {
            'pay_period_start': forms.DateInput(attrs={'type': 'date'}),
            'pay_period_end': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }