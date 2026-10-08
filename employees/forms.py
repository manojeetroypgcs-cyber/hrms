from django import forms
from .models import Employee, EmployeeFamily, EmployeeDocument


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'user', 'employee_code', 'department', 'designation', 'manager',
            'date_of_birth', 'gender', 'address', 'emergency_contact',
            'hire_date', 'employment_status', 'salary',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class EmployeeFamilyForm(forms.ModelForm):
    class Meta:
        model = EmployeeFamily
        fields = ['full_name', 'relationship', 'date_of_birth', 'contact_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ['title', 'file']