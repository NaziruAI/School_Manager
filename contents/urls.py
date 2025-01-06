from django.urls import path
from . import views

app_name = 'contents'

urlpatterns = [
    path('<int:course_id>/', views.course_contents, name='course_contents'),
]
