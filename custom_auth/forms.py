# custom_auth/forms.py
from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'designation', 'first_name', 'last_name', 'email']
