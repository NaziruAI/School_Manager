from django.urls import path
from . import views

app_name = 'courses'  # Namespace for this app

urlpatterns = [
    path('courses/', views.courses, name='courses'),  # View to list all courses
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),  # Detail view
]
