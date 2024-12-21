from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    roles = [
        ('admin', 'Admin'),
        ('team_leader', 'Team Leader'),
        ('staff', 'Staff')
    ]
    role = forms.ChoiceField(choices=roles)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

