from django.shortcuts import render, get_object_or_404
from courses.models import Course

def course_contents(request, course_id):
    # Fetch the course and related contents
    course = get_object_or_404(Course, id=course_id)
    contents = course.contents.all()

    # Render the contents in a template
    return render(request, 'contents/course_contents.html', {'course': course, 'contents': contents})
