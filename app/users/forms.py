from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [ 
            'email',
            'full_name',
            'registration_number',
            'password1', 
            'password2',
            'is_head' 
            ]