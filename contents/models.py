from django.db import models
from django.contrib.auth.models import User


class Content(models.Model):
    # Content metadata
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    content_type_choices = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    content_type = models.CharField(max_length=10, choices=content_type_choices)

    # Related to a course and the user who uploaded it
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='contents')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # File or text content
    text_content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='content/images/', blank=True, null=True)
    video = models.FileField(upload_to='content/videos/', blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
