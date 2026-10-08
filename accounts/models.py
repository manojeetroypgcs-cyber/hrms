from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('HR', 'HR Manager'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def is_admin(self):
        return self.role == 'ADMIN'

    def is_hr(self):
        return self.role in ['ADMIN', 'HR']

    def is_manager(self):
        return self.role in ['ADMIN', 'HR', 'MANAGER']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"