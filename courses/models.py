from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,  # This makes it non-nullable
        default=1,  # Assigns default value (user with ID 1)
        )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
