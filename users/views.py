from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
	"""Log the user out."""
	logout(request)
	return HttpResponseRedirect(reverse('main:home'))


def register(request):
	"""Register a new user."""
	if request.method != 'POST':
		# Display blank registration form.
		form = UserCreationForm()
	else:
		# Process completed form.
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			new_user = form.save()
			# Log the user in and then redirect to home page.
			authenticated_user = authenticate(username=new_user.username,
			password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('main:home'))
	context = {'form': form}
	return render(request, 'users/register.html', context)


# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

def admin_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True       # Admin access
            user.is_superuser = True   # Full admin rights
            user.save()
            # Redirect to admin login after successful signup
            return redirect('admin:login')
    else:
        form = UserCreationForm()

    return render(request, 'users/admin_signup.html', {'form': form})


# Custom admin redirection view
@staff_member_required  # Ensures only logged-in admin/staff can access it
def admin_redirect_view(request):
    return redirect('/admin/')  # Redirect to the admin panel