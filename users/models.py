from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields if necessary
    role_choices = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=role_choices, default='user')

    def __str__(self):
        return self.username
