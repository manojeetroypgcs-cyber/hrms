from django.contrib import admin
from .models import JobPosting, Candidate, Application


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'openings', 'posted_date', 'status')
    list_filter = ('status', 'department', 'posted_date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'posted_date'


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'current_company', 'experience_years', 'status')
    list_filter = ('status', 'experience_years')
    search_fields = ('full_name', 'email', 'current_company')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'applied_date', 'status')
    list_filter = ('status', 'applied_date')
    search_fields = ('candidate__full_name', 'candidate__email', 'job__title')
    date_hierarchy = 'applied_date'