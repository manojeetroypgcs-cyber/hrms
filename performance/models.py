from django.db import models
from employees.models import Employee
from accounts.models import User


class PerformanceReview(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('ACKNOWLEDGED', 'Acknowledged'),
    )

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='performance_reviews'
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviews_given'
    )
    review_period = models.CharField(max_length=50)
    review_date = models.DateField()

    overall_rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    goals_next_period = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-review_date']

    def __str__(self):
        return f"{self.employee.employee_code} - {self.review_period} ({self.overall_rating}/5)"