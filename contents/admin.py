from django.contrib import admin
from .models import Content

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')

admin.site.register(Content, ContentAdmin)
