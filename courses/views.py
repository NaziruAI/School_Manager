from django.shortcuts import render, get_object_or_404
from .models import Course

def courses(request):
    """List all courses."""
    courses = Course.objects.all()
    return render(request, "courses/courses.html", {"courses": courses})

def course_detail(request, course_id):
    """Display details of a specific course."""
    course = get_object_or_404(Course, id=course_id)
    return render(request, "courses/course_detail.html", {"course": course})
