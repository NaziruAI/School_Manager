# contents/admin.py
from django.contrib import admin
from django import forms
from .models import Content

class ContentAdminForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If user is staff, restrict course and uploaded_by fields to readonly
        if self.current_user.is_staff:
            # Disable the dropdowns by making them not editable
            if 'course' in self.fields:
                self.fields['course'].queryset = self.fields['course'].queryset.filter(staff=self.current_user)
            if 'uploaded_by' in self.fields:
                self.fields['uploaded_by'].queryset = self.fields['uploaded_by'].queryset.filter(pk=self.current_user.pk)

    def clean_course(self):
        """
        Ensure the selected course belongs to the staff.
        """
        course = self.cleaned_data.get('course')
        if course and self.current_user.is_staff and course.staff != self.current_user:
            raise forms.ValidationError("You are not allowed to assign contents to this course.")
        return course

    def clean_uploaded_by(self):
        """
        Ensure the user assigns themselves as the uploader.
        """
        uploaded_by = self.cleaned_data.get('uploaded_by')
        if uploaded_by and self.current_user.is_staff and uploaded_by != self.current_user:
            raise forms.ValidationError("You are not allowed to set another user as the uploader.")
        return uploaded_by

class ContentAdmin(admin.ModelAdmin):
    form = ContentAdminForm
    list_display = ('title', 'course', 'uploaded_by', 'content_type', 'created_at')
    search_fields = ('title', 'course__title', 'uploaded_by__username')
    list_filter = ('content_type', 'course')

    def get_form(self, request, obj=None, **kwargs):
        """
        Attach the current user to the form.
        """
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

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
