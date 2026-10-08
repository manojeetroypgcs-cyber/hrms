from django import forms
from .models import PerformanceReview


class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'review_period', 'review_date',
            'overall_rating', 'strengths', 'improvements',
            'goals_next_period', 'status',
        ]
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date'}),
            'strengths': forms.Textarea(attrs={'rows': 3}),
            'improvements': forms.Textarea(attrs={'rows': 3}),
            'goals_next_period': forms.Textarea(attrs={'rows': 3}),
        }