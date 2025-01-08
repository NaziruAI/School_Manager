from django.urls import path, include
from . import views

app_name = 'main'  # This is the namespace

urlpatterns = [
    path('', views.home, name='home'),  # Example route
    path('users/', include(('users.urls', 'users'), namespace='users')),  # Ensure 'include' is used correctly
     path('courses/', include('courses.urls', namespace='courses')),  # Include course app routes
     path('contents/', include('contents.urls', namespace='contents')),
]

from django.conf import settings
from django.conf.urls.static import static

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)