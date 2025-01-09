from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# courses/models.py
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Other fields as required

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
