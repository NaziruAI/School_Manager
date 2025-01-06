from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # If using the default User model, import that instead

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Or 'User' if you're not using a custom model
        fields = ['username', 'email', 'password1', 'password2', 'role']
