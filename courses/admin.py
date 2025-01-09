from django.contrib import admin
from .models import Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'staff', 'description', 'created_at')
    search_fields = ('title',)

    def get_queryset(self, request):
        """
        Restrict staff users to only see their own courses.
        """
        qs = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(staff=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        """
        Allow staff to only change their own courses.
        """
        if obj and not request.user.is_superuser and obj.staff != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """
        Allow staff to only delete their own courses.
        """
        if obj and not request.user.is_superuser and obj.staff != request.user:
            return False
        return super().has_delete_permission(request, obj)

admin.site.register(Course, CourseAdmin)
