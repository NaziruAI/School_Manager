from django.contrib import admin
from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'staff', 'created_at')
    search_fields = ('title', 'staff__username')
    list_filter = ('created_at',)
    
    def get_queryset(self, request):
        """
        Restrict the queryset to only show courses assigned to the logged-in staff.
        """
        qs = super().get_queryset(request)
        if request.user.is_staff and not request.user.is_superuser:
            return qs.filter(staff=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        """
        Allow staff to edit only the courses assigned to them.
        """
        if obj and obj.staff != request.user:
            return False
        return super().has_change_permission(request, obj=obj)

    def has_delete_permission(self, request, obj=None):
        """
        Allow staff to delete only the courses assigned to them.
        """
        if obj and obj.staff != request.user:
            return False
        return super().has_delete_permission(request, obj=obj)

    def has_add_permission(self, request):
        """
        Limit course creation to superusers or other specified criteria.
        """
        return request.user.is_superuser


admin.site.register(Course, CourseAdmin)
