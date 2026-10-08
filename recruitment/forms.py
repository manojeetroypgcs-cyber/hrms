from django import forms
from .models import JobPosting, Candidate, Application


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title', 'department', 'description', 'requirements',
            'location', 'openings', 'posted_date', 'closing_date', 'status',
        ]
        widgets = {
            'posted_date': forms.DateInput(attrs={'type': 'date'}),
            'closing_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
        }


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'full_name', 'email', 'phone', 'resume',
            'current_company', 'experience_years', 'notes', 'status',
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job', 'candidate', 'status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }