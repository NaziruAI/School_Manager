# contents/admin.py
from django.contrib import admin
from .models import Content

class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_by', 'content_type', 'created_at')
    search_fields = ('title', 'course__title', 'uploaded_by__username')
    list_filter = ('content_type', 'course')

    def get_queryset(self, request):
        """
        Restrict content items to only the ones uploaded for courses assigned to the staff member.
        """
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs.filter(course__staff=request.user)  # Staff member sees only courses they're assigned to
        return qs

    def has_add_permission(self, request):
        """
        Only staff can add contents to courses they are assigned to.
        """
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        """
        Allow staff to edit contents only for their assigned courses.
        """
        if obj and obj.course.staff != request.user:
            return False  # Deny editing contents for courses assigned to other staff members
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        """
        Allow staff to delete contents only for their assigned courses.
        """
        if obj and obj.course.staff != request.user:
            return False  # Deny deleting contents for courses assigned to other staff members
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        """
        Allow staff to view contents only for their assigned courses.
        """
        if obj and obj.course.staff != request.user:
            return False  # Deny viewing contents for courses assigned to other staff members
        return request.user.is_staff

admin.site.register(Content, ContentAdmin)
