from django.contrib import admin
from .models import PerformanceReview


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'review_period', 'overall_rating', 'status', 'review_date')
    list_filter = ('status', 'review_period', 'review_date')
    search_fields = (
        'employee__employee_code',
        'employee__user__first_name',
        'employee__user__last_name',
    )
    date_hierarchy = 'review_date'