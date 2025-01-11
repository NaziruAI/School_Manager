from django.contrib import admin
from django import forms
from .models import Content


class ContentAdminForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'current_user') and self.current_user.is_staff and not self.current_user.is_superuser:
            # Staff-specific restrictions
            if 'course' in self.fields:
                self.fields['course'].queryset = self.fields['course'].queryset.filter(staff=self.current_user)
            if 'uploaded_by' in self.fields:
                self.fields['uploaded_by'].queryset = self.fields['uploaded_by'].queryset.filter(pk=self.current_user.pk)

    def clean_course(self):
        """
        Ensure staff assigns content to their own courses. Superusers can assign to any course.
        """
        course = self.cleaned_data.get('course')
        if self.current_user.is_staff and not self.current_user.is_superuser:
            if course and course.staff != self.current_user:
                raise forms.ValidationError("You are not allowed to assign contents to this course.")
        return course

    def clean_uploaded_by(self):
        """
        Ensure staff assigns themselves as the uploader. Superusers can set any uploader.
        """
        uploaded_by = self.cleaned_data.get('uploaded_by')
        if self.current_user.is_staff and not self.current_user.is_superuser:
            if uploaded_by and uploaded_by != self.current_user:
                raise forms.ValidationError("You are not allowed to set another user as the uploader.")
        return uploaded_by


class ContentAdmin(admin.ModelAdmin):
    form = ContentAdminForm
    list_display = ('title', 'course', 'uploaded_by', 'content_type', 'created_at')
    search_fields = ('title', 'course__title', 'uploaded_by__username')
    list_filter = ('content_type', 'course')

    def get_form(self, request, obj=None, **kwargs):
        """
        Attach the current user to the form for context-specific filtering.
        """
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def get_queryset(self, request):
        """
        Provide a filtered queryset based on user type:
        - Superusers see all contents.
        - Staff members see contents only for their assigned courses.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superuser sees all contents
        if request.user.is_staff:
            return qs.filter(course__staff=request.user)  # Restrict to courses assigned to the staff member
        return qs.none()  # Non-staff users can't see any content

    def has_add_permission(self, request):
        """
        Allow staff to add content to their own courses. Superusers can add content to any course.
        """
        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        """
        Allow superusers to change all content, while staff can only change content for their assigned courses.
        """
        if request.user.is_superuser:
            return True  # Superusers can edit all content
        if obj and obj.course.staff != request.user:
            return False  # Staff cannot edit content outside of their assigned courses
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        """
        Allow superusers to delete all content, while staff can only delete content for their assigned courses.
        """
        if request.user.is_superuser:
            return True  # Superusers can delete all content
        if obj and obj.course.staff != request.user:
            return False  # Staff cannot delete content outside of their assigned courses
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        """
        Allow superusers to view all content, while staff can only view content for their assigned courses.
        """
        if request.user.is_superuser:
            return True  # Superusers can view all content
        if obj and obj.course.staff != request.user:
            return False  # Staff cannot view content outside of their assigned courses
        return request.user.is_staff


admin.site.register(Content, ContentAdmin)
