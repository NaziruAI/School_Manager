from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect

# Custom admin redirection view
@staff_member_required  # Ensures only logged-in admin/staff can access it
def admin_redirect_view(request):
    return redirect('/admin/')  # Redirect to the admin panel

app_name = 'users'

urlpatterns = [
    path('dashboard/', admin_redirect_view, name='admin_dashboard'),
    path('admin-signup/', views.admin_signup, name='admin_signup'),
    # login page
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    # Logout page
	path('logout/', views.logout_view, name='logout'),
    # registration page
	path('register/', views.register, name='register'),

]


